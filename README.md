# 🎙️ Voice Notes → Task Extractor

A small project to turn messy voice notes into structured tasks using open-source LLMs.

---

## What is this?

I tend to dump thoughts as voice notes — reminders, random tasks, ideas — and they’re usually unstructured.

This project tries to fix that.

The idea is simple:
- Take a voice note
- Convert it to text
- Extract useful tasks (with date, time, priority)
- Store everything in a clean format

---

## How it works

1. Record voice notes
2. Convert speech → text (Whisper)
3. Send text to an LLM (via Ollama)
4. Get structured output (JSON)

---

## Project structure

```
voice-task-extractor/

data/
  raw_audio/        # voice recordings
  transcripts/      # text versions of audio
  dataset.json      # labeled examples

src/
  stt.py            # speech-to-text
  extractor.py      # LLM task extraction
  utils.py

outputs/
  results.json

README.md
requirements.txt
```

---

## Example

**Input:**
```
Remind me to submit the assignment tomorrow at 5pm
```

**Output:**
```json
{
  "task": "Submit assignment",
  "date": "2026-04-23",
  "time": "17:00",
  "priority": "medium"
}
```

---

## Tech stack

- Python  
- Whisper (for speech-to-text)  
- Ollama (to run open-source LLMs like Mistral / LLaMA)  
- JSON for storing data  

---

## Setup

```bash
git clone https://github.com/your-username/voice-task-extractor.git
cd voice-task-extractor

pip install -r requirements.txt
```

Run the extractor:

```bash
python src/extractor.py
```

---

## Current plan

**Phase 1 — Dataset**
- Create ~100 examples manually
- Store them in JSON

**Phase 2 — Pipeline**
- Hook up Whisper
- Connect LLM through Ollama
- Extract tasks reliably

**Phase 3 — Evaluation**
- Compare outputs vs ground truth
- Improve prompts / logic

---

## Why I’m building this

Mostly to:
- learn how LLM pipelines actually work end-to-end  
- work with real (messy) data instead of clean datasets  
- build something useful for daily life  

---

## Notes

- No fine-tuning (at least initially)
- Focus is on prompt engineering + pipeline design
- Might expand to calendar integration later

---

## License

MIT
