import os
import subprocess
import sys
import uuid

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

VIDEO_INPUT = sys.argv[1]   # pass original video path
AUDIO_INPUT = os.path.join(BASE_DIR, "generated_audio", "translated.wav")

unique_id = str(uuid.uuid4())
VIDEO_OUTPUT = os.path.join(BASE_DIR, "output_videos", f"{unique_id}_translated.mp4")

os.makedirs(os.path.join(BASE_DIR, "output_videos"), exist_ok=True)

if not os.path.exists(VIDEO_INPUT):
    raise FileNotFoundError("Input video not found.")

if not os.path.exists(AUDIO_INPUT):
    raise FileNotFoundError("Translated audio not found.")

command = [
    "ffmpeg",
    "-y",
    "-i", VIDEO_INPUT,
    "-i", AUDIO_INPUT,
    "-map", "0:v:0",
    "-map", "1:a:0",
    "-c:v", "copy",
    "-c:a", "aac",
    "-shortest",
    VIDEO_OUTPUT
]

subprocess.run(command, check=True)

print(VIDEO_OUTPUT)