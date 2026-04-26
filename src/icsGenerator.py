import json
from pathlib import Path
from ics import Calendar, Event

INPUT_FILE = Path("data/structured_output.json")
OUTPUT_FILE = Path("output/echonote_calendar.ics")


def generate_ics_for_calendar(entry):
    # Create output directory if it doesn't exist
    OUTPUT_FILE.parent.mkdir(exist_ok=True)

    # Load existing calendar or create new one if file doesn't exist
    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            calendar = Calendar(f.read())
    else:
        calendar = Calendar()

    # Check if entry should be added to calendar
    intent = entry.get("intent", "")
    normalized = entry.get("normalized_output", {})

    if intent not in ["create_calendar_event", "create_reminder"]:
        return

    # Extract event details from normalized output
    start_datetime = normalized.get("start_datetime", "")
    title = normalized.get("title", "")

    if not start_datetime or not title:
        return

    # Build event with extracted data
    event = Event()
    event.name = title
    event.begin = start_datetime

    # Add end time if available
    end_datetime = normalized.get("end_datetime", "")
    if end_datetime:
        event.end = end_datetime

    # Add transcript and notes to event description
    notes = entry.get("notes", "")
    transcript = entry.get("transcript", "")
    event.description = f"Transcript: {transcript}\nNotes: {notes}"

    # Add event to calendar and write back to file
    calendar.events.add(event)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.writelines(calendar)


def main():
    # Legacy batch mode: regenerate calendar from all entries
    OUTPUT_FILE.parent.mkdir(exist_ok=True)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        entries = json.load(f)

    calendar = Calendar()

    for entry in entries:
        intent = entry.get("intent", "")
        normalized = entry.get("normalized_output", {})

        if intent not in ["create_calendar_event", "create_reminder"]:
            continue

        start_datetime = normalized.get("start_datetime", "")
        title = normalized.get("title", "")

        if not start_datetime or not title:
            continue

        event = Event()
        event.name = title
        event.begin = start_datetime

        end_datetime = normalized.get("end_datetime", "")
        if end_datetime:
            event.end = end_datetime

        notes = entry.get("notes", "")
        transcript = entry.get("transcript", "")
        event.description = f"Transcript: {transcript}\nNotes: {notes}"

        calendar.events.add(event)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.writelines(calendar)

    print(f"Calendar file created: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()