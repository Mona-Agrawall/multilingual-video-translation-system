from gtts import gTTS
import os
import sys
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_TEXT = os.path.join(BASE_DIR, "translated_text", "translated.txt")
OUTPUT_AUDIO = os.path.join(BASE_DIR, "generated_audio", "translated.wav")
TEMP_MP3 = os.path.join(BASE_DIR, "generated_audio", "temp.mp3")

os.makedirs(os.path.join(BASE_DIR, "generated_audio"), exist_ok=True)

if not os.path.exists(INPUT_TEXT):
    raise FileNotFoundError("Translated text not found.")

if len(sys.argv) < 2:
    raise ValueError("Target language not provided.")

target_language = sys.argv[1]

with open(INPUT_TEXT, "r", encoding="utf-8") as f:
    text = f.read()

tts = gTTS(text=text, lang=target_language, slow=False)
tts.save(TEMP_MP3)

subprocess.run(
    ["ffmpeg", "-y", "-i", TEMP_MP3, OUTPUT_AUDIO],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

print("Speech generated successfully.")