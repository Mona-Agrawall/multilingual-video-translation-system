import ffmpeg
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_VIDEO = os.path.join(BASE_DIR, "input_videos", "input.mp4")
OUTPUT_AUDIO = os.path.join(BASE_DIR, "extracted_audio", "audio.wav")

os.makedirs(os.path.join(BASE_DIR, "extracted_audio"), exist_ok=True)

if not os.path.exists(INPUT_VIDEO):
    raise FileNotFoundError(f"Input video not found at: {INPUT_VIDEO}")

ffmpeg.input(INPUT_VIDEO).output(
    OUTPUT_AUDIO,
    ac=1,
    ar=16000,
    format="wav"
).run(overwrite_output=True)

print("Audio extracted successfully.")