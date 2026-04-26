# 🎙️ EchoNote

EchoNote turns your voice notes into structured, actionable data. You speak naturally, and it figures out what you meant, when you meant it, and who was involved — then hands you back clean JSON you can actually do something with.

---

## What problem does it solve?

Most people dump quick thoughts as voice notes — a reminder to call someone, a meeting to schedule, a task to finish later. The problem is those notes just sit there as raw audio. EchoNote listens to them and converts that messy spoken language into organized information a computer can understand and act on.

---

## How it works

The pipeline has three stages:

1. **Transcription** — Your audio file is fed into [Whisper](https://github.com/openai/whisper) (via `faster-whisper`), which converts the speech to text.

2. **Extraction** — The transcript is sent to a local language model running through [Ollama](https://ollama.com). The model reads a carefully written prompt and returns a structured JSON object containing the intent, date, time, participants, location, and anything else it can find in what you said.

3. **Post-processing** — Relative expressions like "tomorrow", "next Friday", or "8 pm" are converted into precise ISO 8601 datetime values so the output is ready to plug into a calendar, task manager, or any other tool.

---

## Example

Say you record yourself saying:

> *"Remind me to call Mom and Dad at 8 o'clock today."*

EchoNote produces:

```json
{
  "id": "0003",
  "speaker": "sourabh",
  "transcript": "Remind me to call Mom and Dad at 8 o'clock today.",
  "intent": "create_reminder",
  "domain": "personal",
  "entities": {
    "title": "Call Mom and Dad",
    "date": "today",
    "time": "20:00",
    "participants": ["Mom", "Dad"],
    "location": "",
    "notes": ""
  },
  "normalized_output": {
    "title": "Call Mom and Dad",
    "start_datetime": "2025-01-15T20:00:00",
    "end_datetime": "",
    "duration_minutes": "",
    "participants": ["Mom", "Dad"],
    "location": ""
  },
  "needs_clarification": false,
  "notes": ""
}
```

If something important is missing — like a date or a time — the output will include `"needs_clarification": true` so you know to follow up.

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
  recordings/               # Raw audio files (not committed)

prompts/
  extraction_prompt.txt     # The instruction template sent to the LLM

src/
  extractor.py              # Calls the Ollama API and returns structured JSON
  postprocess.py            # Converts relative dates/times to ISO format

tools/
  transcribe.py             # Transcribes one or more audio files using Whisper
```

---

## Setup and usage

### Prerequisites

- Python 3.9+
- [Ollama](https://ollama.com) installed and running locally
- The model pulled: `ollama pull qwen2.5:7b`

### Transcribe audio

Pass one or more audio files to the transcription script:

```bash
python tools/transcribe.py data/recordings/0001.m4a
```

You can transcribe multiple files at once by listing them separated by spaces:

```bash
python tools/transcribe.py data/recordings/0001.m4a data/recordings/0002.m4a
```

### Extract structured data

Run the extractor directly to test a single transcript:

```bash
python src/extractor.py
```

This runs a built-in sample ("Remind me to call mom tomorrow at 8 pm") and prints the resulting JSON to the terminal.

---

## Tech stack

- **Python** — the whole pipeline is in Python
- **faster-whisper** — fast, CPU-friendly speech-to-text based on OpenAI's Whisper
- **Ollama** — runs large language models locally (currently using `qwen2.5:7b`)
- **JSON** — the output format throughout

---

## What's next

- Build a larger, more varied dataset of voice note examples
- Make intent and entity extraction more reliable across edge cases
- Potentially connect the output to an actual calendar or task app

---

## Why this exists

This project is a way to learn how real LLM pipelines work end-to-end — dealing with messy, real-world input like spoken language, not clean benchmark data. The goal is to keep it simple, avoid fine-tuning, and focus on understanding the pieces before adding complexity.

---

## License

MIT
