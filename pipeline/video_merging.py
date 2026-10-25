"""Step 6: put the translated speech back into the original video."""

from .media import run_ffmpeg


def merge_audio_into_video(video_path, audio_path, output_path):
    """Replace the video's soundtrack with the given audio, keeping the picture untouched."""
    run_ffmpeg(
        "-i", video_path,
        "-i", audio_path,
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "copy",
        "-c:a", "aac",
        output_path,
    )
