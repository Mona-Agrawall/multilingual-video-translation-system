from googletrans import Translator
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_TEXT = os.path.join(BASE_DIR, "transcripts", "transcript.txt")
OUTPUT_TEXT = os.path.join(BASE_DIR, "translated_text", "translated.txt")

os.makedirs(os.path.join(BASE_DIR, "translated_text"), exist_ok=True)

if not os.path.exists(INPUT_TEXT):
    raise FileNotFoundError("Transcript not found.")

# Get language from command line
if len(sys.argv) < 2:
    raise ValueError("Target language not provided.")

target_language = sys.argv[1]

translator = Translator()

with open(INPUT_TEXT, "r", encoding="utf-8") as f:
    text = f.read()

translated = translator.translate(text, src="en", dest=target_language)

with open(OUTPUT_TEXT, "w", encoding="utf-8") as f:
    f.write(translated.text)

print("Text translated successfully.")