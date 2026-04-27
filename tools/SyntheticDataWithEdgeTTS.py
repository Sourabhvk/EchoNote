import subprocess
from pathlib import Path

INPUT_FILE = "tools/edge_tts_voice_note_mapping_200.txt"
OUT_DIR = Path("S:/echonote/recordings")  # ← S DRIVE
OUT_DIR.mkdir(parents=True, exist_ok=True)

VOICES = [
    "en-IN-PrabhatNeural",
    "en-IN-NeerjaNeural",
    "en-US-GuyNeural",
    "en-US-JennyNeural"
]

lines = []
with open(INPUT_FILE, encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

total = len(lines) * 2
counter = 1

print(f"\n🚀 Starting generation of {total} voice notes...\n")

for pass_num in range(2):
    print(f"\n🔁 PASS {pass_num + 1}/2\n")

    for i, line in enumerate(lines):
        filename, text = line.split("|", 1)
        voice = VOICES[(i + pass_num) % 4]

        out_name = f"{counter:04d}.m4a"
        temp_mp3 = OUT_DIR / f"{counter:04d}.mp3"
        final_m4a = OUT_DIR / out_name

        print(f"[{counter}/{total}] 🎤 Generating → {out_name}")
        print(f"   Voice: {voice}")
        print(f"   Text: {text[:50]}...")

        subprocess.run([
            "edge-tts",
            "--voice", voice,
            "--text", text,
            "--write-media", str(temp_mp3)
        ], check=True)

        print(f"   ✅ MP3 created")

        subprocess.run([
            "ffmpeg",
            "-y",
            "-i", str(temp_mp3),
            "-c:a", "aac",
            str(final_m4a)
        ], check=True)

        print(f"   🔁 Converted → M4A")

        temp_mp3.unlink()
        print(f"   🧹 Temp cleaned\n")

        counter += 1

print("\n🎉 DONE! All 400 voice notes generated.\n")