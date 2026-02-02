import whisper
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

AUDIO_PATH = os.path.join(BASE_DIR, "extracted_audio", "audio.wav")
OUTPUT_TEXT = os.path.join(BASE_DIR, "transcripts", "transcript.txt")

os.makedirs(os.path.join(BASE_DIR, "transcripts"), exist_ok=True)

if not os.path.exists(AUDIO_PATH):
    raise FileNotFoundError("audio.wav not found. Run extract_audio.py first.")

model = whisper.load_model("base")
result = model.transcribe(AUDIO_PATH)

with open(OUTPUT_TEXT, "w", encoding="utf-8") as f:
    f.write(result["text"])

print("Speech converted to text successfully.")