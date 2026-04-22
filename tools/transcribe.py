from faster_whisper import WhisperModel
#give me the tool that can transcribe audio
import sys
#Lets your script read inputs from terminal - we pass audio file via cmd

model = WhisperModel("base", device="cpu", compute_type="int8")
#Load the model - we use the "base" model, run it on CPU, and use int8 quantization for faster inference

audio = sys.argv[1]
#Get the audio file path from the command line arguments i.e. terminal

segments, info = model.transcribe(audio)
#Transcribe the audio file and get the segments and info. The segments contain the transcribed text and timestamps, while info contains metadata about the transcription process.

for segment in segments:
    print(segment.text)
    #Print the transcribed text for each segment to the terminal. Each segment corresponds to a portion of the audio file, and the text is the transcription of that portion.