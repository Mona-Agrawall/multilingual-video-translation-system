from deep_translator import GoogleTranslator
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_TEXT  = os.path.join(BASE_DIR, "transcripts", "transcript.txt")
OUTPUT_TEXT = os.path.join(BASE_DIR, "translated_text", "translated.txt")

os.makedirs(os.path.join(BASE_DIR, "translated_text"), exist_ok=True)

if not os.path.exists(INPUT_TEXT):
    raise FileNotFoundError("Transcript not found. Run speech_to_text.py first.")

if len(sys.argv) < 2:
    raise ValueError("Target language not provided.")

target_language = sys.argv[1]

with open(INPUT_TEXT, "r", encoding="utf-8") as f:
    text = f.read().strip()

# deep-translator handles long text by chunking automatically
translated = GoogleTranslator(source="auto", target=target_language).translate(text)

with open(OUTPUT_TEXT, "w", encoding="utf-8") as f:
    f.write(translated)

print("Text translated successfully.")