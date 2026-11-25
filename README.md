# yt-transcribe

Transcribe YouTube videos or local video/audio files to text. Uses [faster-whisper](https://github.com/SYSTRAN/faster-whisper), runs offline, no API key needed.

```
python transcribe.py https://www.youtube.com/watch?v=abc123
```

Works with:
- YouTube URLs (paste link)
- Local video files (`.mp4`, `.mkv`, `.webm`, etc.)
- Local audio files (`.mp3`, `.wav`, `.m4a`, `.ogg`, etc.)

## Setup

### Windows

1. **Install Python** (skip if you already have it)

   Download from [python.org/downloads](https://www.python.org/downloads/). During install, **check "Add Python to PATH"**.

   Verify:
   ```
   python --version
   ```

2. **Install FFmpeg**

   Download from [gyan.dev/ffmpeg](https://www.gyan.dev/ffmpeg/builds/) → "ffmpeg-release-essentials.zip". Extract it, then add the `bin` folder to your PATH:

   - Extract to `C:\ffmpeg`
   - Search "Environment Variables" in Start menu
   - Under System Variables, find `Path`, click Edit
   - Add `C:\ffmpeg\bin`
   - Click OK, restart your terminal

   Or, if you have [Chocolatey](https://chocolatey.org/) or [winget](https://learn.microsoft.com/en-us/windows/package-manager/winget/):
   ```
   choco install ffmpeg
   ```
   ```
   winget install ffmpeg
   ```

   Verify:
   ```
   ffmpeg -version
   ```

3. **Download this repo**

   ```
   git clone https://github.com/gemimakruva/yt-transcribe.git
   cd yt-transcribe
   ```

   Or download as ZIP from the green "Code" button above → Extract.

4. **Install dependencies**

   ```
   pip install -r requirements.txt
   ```

5. **Done!** See [Usage](#usage) below.

---

### Mac

1. **Install Python** (skip if you already have it)

   ```
   brew install python
   ```

   Or download from [python.org/downloads](https://www.python.org/downloads/).

   Verify:
   ```
   python3 --version
   ```

2. **Install FFmpeg**

   ```
   brew install ffmpeg
   ```

   Verify:
   ```
   ffmpeg -version
   ```

3. **Download this repo**

   ```
   git clone https://github.com/gemimakruva/yt-transcribe.git
   cd yt-transcribe
   ```

4. **Install dependencies**

   ```
   pip3 install -r requirements.txt
   ```

5. **Done!** See [Usage](#usage) below.

> **Note for Mac:** Use `python3` and `pip3` instead of `python` and `pip`.

---

## Usage

### From a YouTube URL

Paste any YouTube link:

```bash
python transcribe.py https://www.youtube.com/watch?v=abc123
```

Also works with short links:

```bash
python transcribe.py https://youtu.be/abc123
```

### From a local video/audio file

```bash
python transcribe.py video.mp4
python transcribe.py interview.mkv
python transcribe.py podcast.mp3
python transcribe.py rekaman.wav
```

### Options

| Option | Description |
|--------|-------------|
| `--model` / `-m` | Whisper model size (default: `base`) |
| `--lang` / `-l` | Language code, e.g. `id`, `en`, `ja` (default: auto-detect) |
| `--output` / `-o` | Output file path (default: `transcript.txt`) |

### Model sizes

| Model | RAM | Speed | Accuracy | Best for |
|-------|-----|-------|----------|----------|
| `tiny` | ~1 GB | Fastest | Rough | Quick preview, clear audio |
| `base` | ~1 GB | Fast | Good | **Default, good enough for most** |
| `small` | ~2 GB | Medium | Solid | Better accuracy, still fast |
| `medium` | ~5 GB | Slow | Great | Important transcripts |
| `large-v3` | ~10 GB | Slowest | Best | Maximum accuracy (needs good hardware) |

### Examples

Transcribe a YouTube video in Indonesian with the small model:

```bash
python transcribe.py https://www.youtube.com/watch?v=abc123 --lang id --model small
```

Transcribe a local MP4 and save to a specific file:

```bash
python transcribe.py meeting.mp4 --output meeting-transcript.txt
```

Auto-detect language from an audio file:

```bash
python transcribe.py podcast.mp3
```

Use the most accurate model:

```bash
python transcribe.py lecture.mp4 --model large-v3 --lang en
```

## Output

The transcript is saved as a text file with timestamps:

```
[00:00 -> 00:03]  Welcome to the show.
[00:03 -> 00:07]  Today we're going to talk about technology.
[00:07 -> 00:12]  Our guest is Dr. Smith from the university.
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: faster_whisper` | Run `pip install faster-whisper` |
| `yt-dlp not found` | Run `pip install yt-dlp` |
| `ffmpeg not found` | Install FFmpeg (see setup above) |
| Transcript accuracy is bad | Try a bigger model: `--model small` or `--model medium` |
| Very slow on my laptop | Use a smaller model: `--model tiny` |
| Wrong language detected | Specify it: `--lang id` or `--lang en` |

## How it works

1. **YouTube URL?** → `yt-dlp` downloads the audio track
2. **Local file?** → Uses the file directly
3. **faster-whisper** loads the model and transcribes the audio offline
4. Output is saved as a timestamped text file

Everything runs locally on your machine. No data is sent to any server.

## License

MIT
