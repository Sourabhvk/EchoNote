from faster_whisper import WhisperModel
#give me the tool that can transcribe audio

import sys
from pathlib import Path
#Lets our script read multiple inputs from terminal and also helps handle file paths cleanly

model = WhisperModel("base", device="cpu", compute_type="int8")
#Load the model - we use the "base" model, run it on CPU, and use int8 quantization for faster inference


def transcribe_file(audio_path):
    #Function to handle transcription of a single file

    segments, info = model.transcribe(audio_path)
    #Transcribe the audio file and get segments and info

    text = " ".join(segment.text.strip() for segment in segments)
    #Combine all segment texts into one clean sentence

    return text.strip()
    #Return final cleaned transcription


if len(sys.argv) < 2:
    print("Usage: python tools/transcribe.py <file1> <file2> ...")
    sys.exit(1)
#Check if we passed any files, else exit


input_files = [Path(p) for p in sys.argv[1:]]
#Get all file paths passed from terminal


for file_path in input_files:
    #Loop through each file one by one

    print(f"filename: {file_path.name}")
    #Print just the file name (not full path)

    if not file_path.exists():
        print("transcription: [FILE NOT FOUND]\n")
        continue
    #If file doesn't exist, skip it and move to next

    transcription = transcribe_file(str(file_path))
    #Call our function to transcribe current file

    print(f"transcription: {transcription}\n")
    #Print transcription in desired format