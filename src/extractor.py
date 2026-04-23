import subprocess
import json

def load_prompt(id, audio_file, speaker, transcript):
    # Read the reusable prompt template from disk.
    with open("prompts/extraction_prompt.txt", "r") as f:
        template = f.read()

    # Replace only known placeholders so JSON braces in the prompt stay untouched.
    prompt = template
    prompt = prompt.replace("{id}", str(id))
    prompt = prompt.replace("{audio_file}", str(audio_file))
    prompt = prompt.replace("{speaker}", str(speaker))
    prompt = prompt.replace("{transcript}", str(transcript))
    return prompt


def extract(id, audio_file, speaker, transcript):
    # Build the final prompt text that will be sent to Ollama.
    prompt = load_prompt(id, audio_file, speaker, transcript)

    # Run the local model and capture its text output.
    result = subprocess.run(
        ["ollama", "run", "llama3.2:3b"],
        input=prompt,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    try:
        # Expect model output to be valid JSON and parse it.
        return json.loads(result.stdout.strip())
    except:
        # If parsing fails, return raw model output for debugging.
        return {"error": "invalid json", "raw": result.stdout}


if __name__ == "__main__":
    # Quick local test with one sample transcript.
    output = extract(
        "0001",
        "data/recordings/0001.m4a",
        "sourabh",
        "Remind me to call mom tomorrow at 8 pm"
    )
    print(output)