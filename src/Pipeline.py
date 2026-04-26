import json
from pathlib import Path

from faster_whisper import WhisperModel
from extractor import extract
from icsGenerator import generate_ics_for_calendar


RECORDINGS_DIR = Path("data/recordings")
SAMPLES_FILE = Path("data/structured_output.json")
SPEAKER = "sourabh"

# Load Whisper speech-to-text model
model = WhisperModel("base", device="cpu")


def transcribe_audio(audio_file):
    # Transcribe audio file to text using Whisper model
    segments, _ = model.transcribe(str(audio_file))

    transcript = ""
    # Concatenate all segment text into single transcript
    for segment in segments:
        transcript += segment.text

    return transcript.strip()


def load_samples():
    # Initialize output file with empty array if it doesn't exist
    if not SAMPLES_FILE.exists():
        SAMPLES_FILE.parent.mkdir(parents=True, exist_ok=True)
        save_samples([])
        return []

    # Load existing samples from JSON file
    with open(SAMPLES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_samples(samples):
    # Serialize and write samples array to JSON file with pretty formatting
    with open(SAMPLES_FILE, "w", encoding="utf-8") as f:
        json.dump(samples, f, indent=2)


def main():
    # Load previously processed samples to check for duplicates
    samples = load_samples()

    # Collect and sort all .m4a audio files from recordings directory
    audio_files = sorted(RECORDINGS_DIR.glob("*.m4a"))

    if not audio_files:
        print("No audio files found in data/recordings")
        return

    # Build set of already-processed audio file paths for duplicate detection
    existing_audio_files = {
        sample.get("audio_file") for sample in samples if sample.get("audio_file")
    }

    # Process each new audio file through the pipeline
    for audio_file in audio_files:
        # Normalize path to forward slashes for consistent storage
        audio_path = str(audio_file).replace("\\", "/")
        # Use audio filename stem (without extension) as stable ID
        entry_id = audio_file.stem

        if audio_path in existing_audio_files:
            print(f"Skipping already processed file: {audio_path}")
            continue

        print(f"Transcribing: {audio_path}")
        transcript = transcribe_audio(audio_file)

        print(f"Extracting JSON for: {entry_id}")
        # Send transcript to Ollama model and get structured JSON output
        extracted = extract(
            id=entry_id,
            audio_file=audio_path,
            speaker=SPEAKER,
            transcript=transcript
        )

        samples.append(extracted)
        save_samples(samples)

        print(f"JSON ready for {entry_id}, creating ICS event...")
        # Add event to calendar if it's a calendar/reminder entry
        generate_ics_for_calendar(extracted)

        print(f"Added entry {entry_id} to data/structured_output.json")


if __name__ == "__main__":
    main()