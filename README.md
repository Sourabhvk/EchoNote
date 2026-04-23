🎙️ EchoNote — Voice → Action

A small project to turn messy voice notes into structured, usable actions.

What is this?

I usually dump thoughts as voice notes — reminders, plans, random tasks — and they’re all over the place.

EchoNote tries to fix that by turning voice into something structured.

What it does
Converts voice notes → text
Understands intent (event / reminder / task / etc.)
Extracts key details (time, date, people)
Outputs clean JSON

Basically:
voice → structured action

How it works
Record voice note
Transcribe (Whisper)
Parse with LLM (Ollama)
Output structured JSON
Example

Input:

Meet ABC tomorrow at 9 PM for drinks

Output:

{
  "intent": "create_calendar_event",
  "title": "Drinks with ABC",
  "date": "tomorrow",
  "time": "21:00"
}
Tech stack
Python
Whisper (speech-to-text)
Ollama (LLMs like LLaMA / Mistral)
JSON
Project structure
data/
  recordings/
  dataset.json

tools/
  transcribe.py

Run transcription
python tools/transcribe.py data/recordings/0001.m4a
Plan
Build small dataset (mixed voice notes)
Extract intent + entities reliably
Output clean JSON
Maybe hook into calendar later
Why I’m building this
learn real LLM pipelines
work with messy input (actual voice)
build something I’d actually use
Notes
keeping it simple
no fine-tuning (for now)
focus on understanding > complexity
License

MIT