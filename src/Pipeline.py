import json
from pathlib import Path

from faster_whisper import WhisperModel
from extractor import extract


RECORDINGS_DIR = Path("data/recordings")
SAMPLES_FILE = Path("data/samples.json")
SPEAKER = "sourabh"

model = WhisperModel("base", device="cpu")


def transcribe_audio(audio_file):
    segments, _ = model.transcribe(str(audio_file))

    transcript = ""
    for segment in segments:
        transcript += segment.text

    return transcript.strip()


def load_samples():
    if not SAMPLES_FILE.exists():
        SAMPLES_FILE.parent.mkdir(parents=True, exist_ok=True)
        save_samples([])
        return []

    with open(SAMPLES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_samples(samples):
    with open(SAMPLES_FILE, "w", encoding="utf-8") as f:
        json.dump(samples, f, indent=2)

def main():
    samples = load_samples()

    audio_files = sorted(RECORDINGS_DIR.glob("*.m4a"))

    if not audio_files:
        print("No audio files found in data/recordings")
        return

    existing_audio_files = {
        sample.get("audio_file") for sample in samples if sample.get("audio_file")
    }

    for audio_file in audio_files:
        audio_path = str(audio_file).replace("\\", "/")
        entry_id = audio_file.stem

        if audio_path in existing_audio_files:
            print(f"Skipping already processed file: {audio_path}")
            continue

        print(f"Transcribing: {audio_path}")
        transcript = transcribe_audio(audio_file)

        print(f"Extracting JSON for: {entry_id}")
        extracted = extract(
            id=entry_id,
            audio_file=audio_path,
            speaker=SPEAKER,
            transcript=transcript
        )

        samples.append(extracted)
        save_samples(samples)

        print(f"Added entry {entry_id} to data/samples.json")


if __name__ == "__main__":
    main()