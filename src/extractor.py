import requests  # Lets Python make HTTP calls to the Ollama API.
import json  # Lets us convert between text and Python dictionaries.
from postprocess import normalize_datetime  # Reuse our date normalization logic to clean up model output dates.

MODEL_NAME = "qwen2.5:7b"  # Single place to change which local model is used.


def load_prompt(id, audio_file, speaker, transcript):  # Build a final prompt string from template + inputs.
    with open("prompts/extraction_prompt.txt", "r", encoding="utf-8") as f:  # Open the reusable prompt file safely as UTF-8 text.
        template = f.read()  # Read the whole prompt template into memory.

    prompt = template  # Start from the raw template text.
    prompt = prompt.replace("{id}", str(id))  # Inject the note id into the template.
    prompt = prompt.replace("{audio_file}", str(audio_file))  # Inject the audio file path/name.
    prompt = prompt.replace("{speaker}", str(speaker))  # Inject the speaker name.
    prompt = prompt.replace("{transcript}", str(transcript))  # Inject the transcript text the model should analyze.

    return prompt  # Return the fully prepared prompt string.


def extract(id, audio_file, speaker, transcript):  # Send prompt to Ollama and return structured JSON output.
    prompt = load_prompt(id, audio_file, speaker, transcript)  # First, generate the final prompt text.

    try:  # Protect network call so timeout/connection failures are handled cleanly.
        response = requests.post(  # Make one HTTP POST request to Ollama's generate endpoint.
            "http://localhost:11434/api/generate",  # Local Ollama API URL.
            json={  # Request body sent as JSON.
                "model": MODEL_NAME,  # Which model Ollama should run.
                "prompt": prompt,  # The instruction + data given to the model.
                "stream": False,  # Ask for one full response instead of token streaming.
                "format": "json"  # Ask the model to format its answer as JSON.
            },  # End of JSON payload.
            timeout=180  # Abort request if Ollama takes longer than 180 seconds.
        )  # End requests.post call.
    except requests.exceptions.Timeout:  # Triggered when request exceeds timeout limit.
        return {"error": "ollama timeout", "raw": "model took more than 180 seconds"}  # Return a clear timeout error payload.
    except requests.exceptions.ConnectionError:  # Triggered when Ollama server cannot be reached.
        return {"error": "ollama not running", "raw": "start Ollama first"}  # Return a clear connection error payload.

    if response.status_code != 200:  # Non-200 means API call failed from HTTP perspective.
        return {  # Return details so debugging is easy.
            "error": "ollama api failed",  # High-level error label.
            "code": response.status_code,  # Actual HTTP status code.
            "raw": response.text  # Raw response text for diagnosis.
        }  # End error response dictionary.

    text = response.json().get("response", "").strip()  # Pull generated text from API JSON and trim whitespace.

    if not text:  # If model returned empty string, this is a failure case.
        return {"error": "empty model output", "raw": text}  # Return an explicit empty-output error.

    try:  # Try converting model text into a Python dictionary/list.
        data = json.loads(text)  # Attempt to parse the model's response as JSON.
        data = normalize_datetime(data)  # Clean up any date/datetime fields in the model output.
        return data  # Return the structured, normalized data extracted from the model.
    
    except json.JSONDecodeError:  # Happens when model text is not valid JSON.
        return {"error": "invalid json", "raw": text}  # Return raw text so you can inspect what model produced.


if __name__ == "__main__":  # Run this block only when executing this file directly.
    output = extract(  # Call extract with a sample test input.
        "0001",  # Sample note id.
        "data/recordings/0001.m4a",  # Sample audio path string.
        "sourabh",  # Sample speaker name.
        "Remind me to call mom tomorrow at 8 pm"  # Sample transcript sentence.
    )  # End sample extract call.

    print(json.dumps(output, indent=2))  # Pretty-print returned dictionary as readable JSON.