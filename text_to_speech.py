import os
import sys
import subprocess
from gtts import gTTS
from pydub import AudioSegment
import math

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_TEXT = os.path.join(BASE_DIR, "translated_text", "translated.txt")
ORIGINAL_AUDIO = os.path.join(BASE_DIR, "extracted_audio", "audio.wav")
OUTPUT_AUDIO = os.path.join(BASE_DIR, "generated_audio", "translated.wav")
TEMP_MP3 = os.path.join(BASE_DIR, "generated_audio", "temp.mp3")
TEMP_WAV = os.path.join(BASE_DIR, "generated_audio", "temp.wav")

os.makedirs(os.path.join(BASE_DIR, "generated_audio"), exist_ok=True)

if len(sys.argv) < 2:
    raise ValueError("Target language not provided.")

target_language = sys.argv[1]

# -------------------------
# Generate TTS
# -------------------------

with open(INPUT_TEXT, "r", encoding="utf-8") as f:
    text = f.read().strip()

tts = gTTS(text=text, lang=target_language, slow=False)
tts.save(TEMP_MP3)

subprocess.run(
    ["ffmpeg", "-y", "-i", TEMP_MP3, TEMP_WAV],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

# -------------------------
# Measure Durations
# -------------------------

original = AudioSegment.from_wav(ORIGINAL_AUDIO)
generated = AudioSegment.from_wav(TEMP_WAV)

original_duration = len(original) / 1000
generated_duration = len(generated) / 1000

print("Original:", original_duration)
print("Generated:", generated_duration)

# -------------------------
# Compute Speed Ratio
# -------------------------

speed = generated_duration / original_duration

# If generated is longer → speed > 1 → we must speed up

# atempo supports 0.5–2.0 only
filters = []

while speed > 2.0:
    filters.append("atempo=2.0")
    speed /= 2.0

while speed < 0.5:
    filters.append("atempo=0.5")
    speed *= 2.0

filters.append(f"atempo={speed}")

atempo_filter = ",".join(filters)

# -------------------------
# Apply True Time Compression
# -------------------------

subprocess.run(
    [
        "ffmpeg",
        "-y",
        "-i", TEMP_WAV,
        "-filter:a", atempo_filter,
        OUTPUT_AUDIO
    ],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

print("Speech generated and duration truly matched.")