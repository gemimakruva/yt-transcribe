#!/usr/bin/env python3
"""
yt-transcribe: Transcribe YouTube videos or local video/audio files to text.

Usage:
    python transcribe.py <youtube-url-or-file> [options]

Examples:
    python transcribe.py https://www.youtube.com/watch?v=abc123
    python transcribe.py video.mp4
    python transcribe.py podcast.mp3 --model medium --lang en
"""

import argparse
import os
import subprocess
import sys
import tempfile
import time

def check_dependencies():
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("Error: faster-whisper not installed.")
        print("Install it with: pip install faster-whisper")
        sys.exit(1)

    if not is_url_input(sys.argv[1] if len(sys.argv) > 1 else ""):
        return

    try:
        subprocess.run(["yt-dlp", "--version"], capture_output=True, check=True)
    except FileNotFoundError:
        print("Error: yt-dlp not installed (required for YouTube URLs).")
        print("Install it with: pip install yt-dlp")
        sys.exit(1)

def is_url_input(source):
    return source.startswith("http://") or source.startswith("https://")

def download_audio(url, output_dir):
    output_path = os.path.join(output_dir, "audio.%(ext)s")
    cmd = [
        "yt-dlp", "-x",
        "--audio-format", "mp3",
        "--audio-quality", "5",
        "-o", output_path,
        url,
    ]
    print(f"Downloading audio from: {url}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error downloading: {result.stderr}")
        sys.exit(1)

    for f in os.listdir(output_dir):
        if f.startswith("audio."):
            return os.path.join(output_dir, f)

    print("Error: downloaded audio file not found.")
    sys.exit(1)

def transcribe(audio_path, model_size, language, output_path):
    from faster_whisper import WhisperModel

    print(f"Loading model: {model_size} ...")
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    print(f"Transcribing: {os.path.basename(audio_path)}")
    print(f"Language: {language or 'auto-detect'}")
    print()

    kwargs = {"beam_size": 5}
    if language:
        kwargs["language"] = language

    segments, info = model.transcribe(audio_path, **kwargs)

    detected = info.language
    prob = info.language_probability
    duration = info.duration
    print(f"Detected language: {detected} (confidence: {prob:.0%})")
    print(f"Duration: {duration/60:.0f}m {duration%60:.0f}s")
    print("-" * 60)

    lines = []
    for seg in segments:
        start_m, start_s = divmod(int(seg.start), 60)
        end_m, end_s = divmod(int(seg.end), 60)
        timestamp = f"[{start_m:02d}:{start_s:02d} -> {end_m:02d}:{end_s:02d}]"
        text = seg.text.strip()
        print(f"{timestamp}  {text}")
        lines.append(f"{timestamp}  {text}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print("-" * 60)
    print(f"Saved to: {output_path}")
    print(f"Total lines: {len(lines)}")

def main():
    parser = argparse.ArgumentParser(
        description="Transcribe YouTube videos or local video/audio files to text.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python transcribe.py https://www.youtube.com/watch?v=abc123
  python transcribe.py https://youtu.be/abc123 --model medium --lang en
  python transcribe.py interview.mp4
  python transcribe.py podcast.mp3 --lang id --output hasil.txt

Models (smallest → largest, slower = more accurate):
  tiny     ~1 GB RAM, fastest, rough accuracy
  base     ~1 GB RAM, good enough for clear audio (default)
  small    ~2 GB RAM, solid accuracy
  medium   ~5 GB RAM, great accuracy
  large-v3 ~10 GB RAM, best accuracy (needs good hardware)
        """,
    )
    parser.add_argument("source", help="YouTube URL or path to a local video/audio file")
    parser.add_argument("--model", "-m", default="base",
                        choices=["tiny", "base", "small", "medium", "large-v3"],
                        help="Whisper model size (default: base)")
    parser.add_argument("--lang", "-l", default=None,
                        help="Language code, e.g. id, en, ja (default: auto-detect)")
    parser.add_argument("--output", "-o", default=None,
                        help="Output file path (default: transcript.txt)")

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    check_dependencies()

    output_path = args.output or "transcript.txt"

    if is_url_input(args.source):
        with tempfile.TemporaryDirectory() as tmpdir:
            audio_path = download_audio(args.source, tmpdir)
            transcribe(audio_path, args.model, args.lang, output_path)
    else:
        if not os.path.isfile(args.source):
            print(f"Error: file not found: {args.source}")
            sys.exit(1)
        transcribe(args.source, args.model, args.lang, output_path)

if __name__ == "__main__":
    main()
