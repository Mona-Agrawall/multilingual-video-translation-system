import ffmpeg
import os
import sys

video_path = sys.argv[1]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_AUDIO = os.path.join(BASE_DIR, "extracted_audio", "audio.wav")

os.makedirs(os.path.join(BASE_DIR, "extracted_audio"), exist_ok=True)

if not os.path.exists(video_path):
    raise FileNotFoundError("Input video not found.")

ffmpeg.input(video_path).output(
    OUTPUT_AUDIO,
    ac=1,
    ar=16000,
    format="wav"
).run(overwrite_output=True)

print("Audio extracted successfully.")