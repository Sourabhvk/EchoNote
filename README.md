# 🎙️ EchoNote

Turns `.m4a` voice notes into structured JSON and `.ics` calendar events using Whisper + a local LLM.

## How it works

1. **Transcribe** — Whisper converts audio to text
2. **Extract** — Ollama LLM pulls intent, date, time, participants, and duration into JSON
3. **Normalize** — Relative dates/times ("tomorrow", "8 pm") become ISO 8601 datetimes
4. **Export** — Reminders and calendar events are written to `output/echonote_calendar.ics`

## Usage

### Prerequisites
- Python 3.9+, [Ollama](https://ollama.com) running locally
- `ollama pull qwen2.5:7b`

### Run the full pipeline

Drop `.m4a` files into `data/recordings/`, then:

```bash
cd src && python Pipeline.py
```

Results are saved to `data/structured_output.json` and `output/echonote_calendar.ics`. Already-processed files are skipped automatically.

### Transcribe only

```bash
python tools/transcribe.py data/recordings/0001.m4a
```

## Supported intents

`create_reminder` · `create_calendar_event` · `create_task` · `query_schedule` · `edit_event` · `cancel_event`

## Project structure

```
src/
  Pipeline.py       # End-to-end runner
  extractor.py      # Ollama API → structured JSON
  postprocess.py    # Date/time/duration normalization
  icsGenerator.py   # .ics calendar export
tools/
  transcribe.py     # Standalone audio transcription
prompts/
  extraction_prompt.txt
data/
  recordings/       # Input audio (not committed)
  structured_output.json
```

## License

MIT
