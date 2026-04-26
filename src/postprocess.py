from datetime import datetime, timedelta  # Needed for building normalized date/time values.
import re  # Used for robust text parsing (time and duration patterns).


WEEKDAYS = {
    "monday": 0,  # Python weekday index for Monday.
    "tuesday": 1,  # Python weekday index for Tuesday.
    "wednesday": 2,  # Python weekday index for Wednesday.
    "thursday": 3,  # Python weekday index for Thursday.
    "friday": 4,  # Python weekday index for Friday.
    "saturday": 5,  # Python weekday index for Saturday.
    "sunday": 6,  # Python weekday index for Sunday.
}


NUMBER_WORDS = {
    "zero": 0,  # Word-to-number map for basic duration parsing.
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "half": 0.5,
    "an": 1,
    "a": 1,
}


def normalize_date(date_text):
    today = datetime.today()  # Read current local date/time once for consistent calculations.

    if not date_text:  # If date is missing/empty, caller can request clarification.
        return ""  # Return empty string to indicate normalization failure.

    text = str(date_text).lower().strip()  # Normalize input for predictable comparisons.

    if text == "today":  # Relative keyword: same day.
        return today.date().isoformat()  # Return YYYY-MM-DD.

    if text == "tomorrow":  # Relative keyword: next day.
        return (today + timedelta(days=1)).date().isoformat()  # Return YYYY-MM-DD.

    if text == "day after tomorrow":  # Extra relative case commonly produced in speech.
        return (today + timedelta(days=2)).date().isoformat()  # Return YYYY-MM-DD.

    if text.startswith("this "):  # Accept forms like "this Thursday".
        text = text.replace("this ", "", 1).strip()  # Keep weekday only.

    is_next = False  # Track whether user explicitly asked for next week.
    if text.startswith("next "):  # Accept forms like "next Monday".
        text = text.replace("next ", "", 1).strip()  # Keep weekday only.
        is_next = True  # Force result to be in the following week.

    if text in WEEKDAYS:  # Handle weekday names.
        target_weekday = WEEKDAYS[text]  # Target weekday index.
        days_ahead = target_weekday - today.weekday()  # Distance from today.

        if days_ahead < 0:  # If weekday already passed this week,
            days_ahead += 7  # roll over into next week.

        if is_next and days_ahead == 0:  # "next Monday" on Monday means 7 days later.
            days_ahead = 7
        elif is_next:  # "next <weekday>" should always refer to following week.
            days_ahead += 7

        return (today + timedelta(days=days_ahead)).date().isoformat()  # Return YYYY-MM-DD.

    return ""  # Unknown date format: leave empty for clarification flow.


def normalize_time(time_text):
    if not time_text:  # Missing time field.
        return ""  # Return empty marker.

    text = str(time_text).lower().strip()  # Normalize casing/spacing.
    text = text.replace(".", "")  # Normalize formats like "p.m." -> "pm".

    if text in {"noon"}:  # Common natural-language alias.
        return "12:00"  # Standard 24-hour value.

    if text in {"midnight"}:  # Common natural-language alias.
        return "00:00"  # Standard 24-hour value.

    # Match variants like 8pm, 8 pm, 08:30 PM, 20:15.
    match = re.match(r"^(\d{1,2})(?::(\d{2}))?\s*(am|pm)?$", text)
    if not match:  # If format is not recognized,
        return ""  # return empty to trigger clarification.

    hour = int(match.group(1))  # Parsed hour number.
    minute = int(match.group(2) or "00")  # Parsed minute number (or default 00).
    meridiem = match.group(3)  # am/pm marker when present.

    if minute < 0 or minute > 59:  # Guard against invalid minute values.
        return ""  # Invalid time.

    if meridiem:  # Convert 12-hour time to 24-hour time.
        if hour < 1 or hour > 12:  # 12-hour clock only allows 1..12.
            return ""
        if meridiem == "am":  # Morning conversion.
            hour = 0 if hour == 12 else hour  # 12 AM -> 00.
        else:  # PM conversion.
            hour = hour if hour == 12 else hour + 12  # Add 12 except for 12 PM.
    else:  # Handle 24-hour input format.
        if hour < 0 or hour > 23:  # Valid 24-hour range check.
            return ""

    return f"{hour:02d}:{minute:02d}"  # Canonical HH:MM output.


def _parse_number_token(token):
    token = token.strip().lower()  # Normalize text before lookup/parsing.

    if token in NUMBER_WORDS:  # Support words like "one", "an", "half".
        return float(NUMBER_WORDS[token])

    try:  # Try direct numeric parsing for values like 30 or 1.5.
        return float(token)
    except ValueError:  # Not a parseable number.
        return None


def normalize_duration(duration_text):
    if not duration_text:  # Missing duration field is valid.
        return ""  # Keep empty to signal "unknown duration".

    text = str(duration_text).lower().strip()  # Normalize casing/spacing.

    if text.isdigit():  # Plain number means minutes by convention.
        return int(text)

    # Accept formats like "1 hour", "1.5 hours", "45 minutes", "an hour".
    match = re.match(r"^(\w+(?:\.\d+)?)\s*(hour|hours|hr|hrs|minute|minutes|min|mins)$", text)
    if not match:  # Unsupported format.
        return ""  # Keep empty to avoid raising exceptions.

    amount = _parse_number_token(match.group(1))  # Parse numeric part.
    unit = match.group(2)  # Parse duration unit.

    if amount is None or amount < 0:  # Invalid numeric value.
        return ""

    if unit in {"hour", "hours", "hr", "hrs"}:  # Convert hour-based values to minutes.
        return int(round(amount * 60))

    return int(round(amount))  # Minute-based units map directly.


def normalize_datetime(extracted_json):
    entities = extracted_json.get("entities", {})  # Safe access to extracted entities map.
    normalized = extracted_json.get("normalized_output", {})  # Preserve existing normalized keys if present.

    title = entities.get("title", "")  # Event/reminder title.
    date_text = entities.get("date", "")  # Raw extracted date text.
    time_text = entities.get("time", "")  # Raw extracted time text.
    duration_text = entities.get("duration", "")  # Raw extracted duration text.

    normalized_date = normalize_date(date_text)  # Convert date text to YYYY-MM-DD.
    normalized_time = normalize_time(time_text)  # Convert time text to HH:MM.
    duration_minutes = normalize_duration(duration_text)  # Convert duration to integer minutes.

    start_datetime = ""  # Default empty start when normalization fails.
    end_datetime = ""  # Default empty end when no valid duration/time.

    if normalized_date and normalized_time:  # Only build start when both date and time are valid.
        start_datetime = f"{normalized_date}T{normalized_time}:00"  # Canonical local datetime string.

    if start_datetime and duration_minutes != "":  # End time requires both start and duration.
        start = datetime.fromisoformat(start_datetime)  # Parse start ISO string.
        end = start + timedelta(minutes=duration_minutes)  # Add duration to compute end.
        end_datetime = end.isoformat(timespec="seconds")  # Serialize with seconds precision.

    normalized["title"] = title  # Persist normalized title.
    normalized["start_datetime"] = start_datetime  # Persist normalized start.
    normalized["end_datetime"] = end_datetime  # Persist normalized end.
    normalized["duration_minutes"] = duration_minutes  # Persist numeric duration when available.
    normalized["participants"] = entities.get("participants", [])  # Carry participants through untouched.
    normalized["location"] = entities.get("location", "")  # Carry location through untouched.

    extracted_json["normalized_output"] = normalized  # Write normalized section back to root payload.

    if not start_datetime:  # If date/time is still incomplete,
        extracted_json["needs_clarification"] = True  # downstream should ask user follow-up question.
        extracted_json["notes"] = "Date or time could not be normalized"  # Human-readable reason.
    else:  # If start datetime is valid,
        extracted_json["needs_clarification"] = False  # no clarification required.
        extracted_json["notes"] = ""  # Clear previous notes.

    return extracted_json  # Return updated object for pipeline chaining.