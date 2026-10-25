"""Small helpers around the FFmpeg command-line tools used by every step."""

import subprocess


def run_ffmpeg(*args):
    """Run an FFmpeg command, overwriting the output file and raising on failure."""
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *map(str, args)], check=True)


def get_duration(media_path):
    """Return the length of an audio or video file in seconds."""
    result = subprocess.run(
        [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(media_path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(result.stdout)
