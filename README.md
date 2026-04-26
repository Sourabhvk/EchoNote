# 🎙️ EchoNote

EchoNote turns your voice notes into structured, actionable data. You speak naturally, and it figures out what you meant, when you meant it, and who was involved — then hands you back clean JSON you can actually do something with, and exports it straight to a `.ics` calendar file.

---

## What problem does it solve?

Most people dump quick thoughts as voice notes — a reminder to call someone, a meeting to schedule, a task to finish later. The problem is those notes just sit there as raw audio. EchoNote listens to them and converts that messy spoken language into organized information a computer can understand and act on.

---

## How it works

The pipeline has four stages:

1. **Transcription** — Audio files in `data/recordings/` are fed into [Whisper](https://github.com/openai/whisper) (via `faster-whisper`), which converts speech to text.

2. **Extraction** — The transcript is sent to a local language model running through [Ollama](https://ollama.com). The model reads a carefully written prompt and returns a structured JSON object containing the intent, date, time, participants, location, duration, and anything else it can find in what you said.

3. **Post-processing** — Relative expressions like "tomorrow", "next Friday", or "8 pm" are converted into precise ISO 8601 datetime values. Durations (e.g. "1 hour", "45 minutes") are normalized to integer minutes, and end datetimes are computed automatically.

4. **Calendar export** — For `create_reminder` and `create_calendar_event` entries, an `.ics` file is generated at `output/echonote_calendar.ics` so you can import the event into any calendar app.

---

## Example

Say you record yourself saying:

> *"Remind me to call Mom and Dad at 8 o'clock today."*

EchoNote produces:

```json
{
  "id": "0003",
  "audio_file": "data/recordings/0003.m4a",
  "speaker": "sourabh",
  "transcript": "Remind me to call Mom and Dad at 8 o'clock today.",
  "intent": "create_reminder",
  "domain": "personal",
  "entities": {
    "title": "call Mom and Dad",
    "date": "today",
    "time": "20:00",
    "start_time": "20:00",
    "end_time": "",
    "duration": "",
    "participants": ["Mom", "Dad"],
    "location": "",
    "notes": ""
  },
  "normalized_output": {
    "title": "call Mom and Dad",
    "start_datetime": "2026-04-27T20:00:00",
    "end_datetime": "",
    "duration_minutes": "",
    "participants": ["Mom", "Dad"],
    "location": ""
  },
  "needs_clarification": false,
  "notes": ""
}
```

The entry is also appended to `data/structured_output.json` and a corresponding event is written to `output/echonote_calendar.ics`.

If something important is missing — like both a date and a time — the output will include `"needs_clarification": true` so you know to follow up.

---

## Supported intents

| Intent | When it's used |
|---|---|
| `create_reminder` | "Remind me to…" — time-based nudges |
| `create_calendar_event` | Meetings, calls, appointments |
| `create_task` | General to-dos with no specific reminder |
| `query_schedule` | Asking what's on the calendar |
| `edit_event` | Changing an existing event |
| `cancel_event` | Cancelling something |

---

## Project structure

```
data/
  samples.json              # Labelled example entries used for development
  structured_output.json    # Pipeline output — all processed entries (auto-created)
  recordings/               # Raw audio files (not committed)

output/
  echonote_calendar.ics     # Generated calendar file (auto-created)

prompts/
  extraction_prompt.txt     # The instruction template sent to the LLM

src/
  Pipeline.py               # End-to-end runner: transcribe → extract → export ICS
  extractor.py              # Calls the Ollama API and returns structured JSON
  postprocess.py            # Converts relative dates/times/durations to ISO format
  icsGenerator.py           # Writes calendar events to an .ics file

tools/
  transcribe.py             # Standalone tool: transcribes one or more audio files
```

---

## Setup and usage

### Prerequisites

- Python 3.9+
- [Ollama](https://ollama.com) installed and running locally
- A model pulled, e.g.:
  ```bash
  ollama pull qwen2.5:7b
  ```

### Run the full pipeline

Drop your `.m4a` recordings into `data/recordings/`, then run:

```bash
cd src
python Pipeline.py
```

The pipeline will:
- Skip any files it has already processed
- Transcribe each new recording with Whisper
- Extract structured JSON via Ollama
- Append each entry to `data/structured_output.json`
- Add calendar events to `output/echonote_calendar.ics`

### Transcribe audio only

Use the standalone transcription tool when you only need text output:

```bash
python tools/transcribe.py data/recordings/0001.m4a
```

You can transcribe multiple files at once:

```bash
python tools/transcribe.py data/recordings/0001.m4a data/recordings/0002.m4a
```

---

## Tech stack

- **Python** — the whole pipeline is in Python
- **faster-whisper** — fast, CPU-friendly speech-to-text based on OpenAI's Whisper
- **Ollama** — runs large language models locally (e.g. `qwen2.5:7b`, `llama3.2:3b`)
- **ics** — generates standard `.ics` calendar files
- **JSON** — the output format throughout

---

## Why this exists

This project is a way to learn how real LLM pipelines work end-to-end — dealing with messy, real-world input like spoken language, not clean benchmark data. The goal is to keep it simple, avoid fine-tuning, and focus on understanding the pieces before adding complexity.

---

## License

MIT
