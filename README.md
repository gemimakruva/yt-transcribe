# yt-transcribe

Transcribe YouTube videos or local video/audio files to text. Uses [faster-whisper](https://github.com/SYSTRAN/faster-whisper), runs offline, no API key needed.

![demo](demo.gif)

Works with:
- YouTube URLs (paste link)
- Local video files (`.mp4`, `.mkv`, `.webm`, etc.)
- Local audio files (`.mp3`, `.wav`, `.m4a`, `.ogg`, etc.)

## Quick Install (copy-paste to terminal)

### Windows (PowerShell)

Open PowerShell and paste:

```powershell
# Install Python (skip if already installed)
winget install Python.Python.3.12

# Install FFmpeg
winget install Gyan.FFmpeg

# Restart PowerShell after installing Python and FFmpeg, then continue:

# Download and setup
git clone https://github.com/gemimakruva/yt-transcribe.git
cd yt-transcribe
pip install -r requirements.txt

# Test it
python transcribe.py --help
```

> No git? Download ZIP from the green "Code" button above, extract, then `cd` into the folder.

### Mac (Terminal)

Open Terminal and paste:

```bash
# Install Homebrew (skip if already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python and FFmpeg
brew install python ffmpeg

# Download and setup
git clone https://github.com/gemimakruva/yt-transcribe.git
cd yt-transcribe
pip3 install -r requirements.txt

# Test it
python3 transcribe.py --help
```

### Linux (Terminal)

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install -y python3 python3-pip ffmpeg git

# Download and setup
git clone https://github.com/gemimakruva/yt-transcribe.git
cd yt-transcribe
pip3 install -r requirements.txt

# Test it
python3 transcribe.py --help
```

---

## Manual Setup (step by step)

<details>
<summary><strong>Windows (detailed)</strong></summary>

1. **Install Python** (skip if you already have it)

   Download from [python.org/downloads](https://www.python.org/downloads/). During install, **check "Add Python to PATH"**.

   Verify in PowerShell:
   ```
   python --version
   ```

2. **Install FFmpeg**

   Option A (recommended, via PowerShell):
   ```
   winget install Gyan.FFmpeg
   ```

   Option B (via [Chocolatey](https://chocolatey.org/)):
   ```
   choco install ffmpeg
   ```

   Option C (manual):
   - Download from [gyan.dev/ffmpeg](https://www.gyan.dev/ffmpeg/builds/) > "ffmpeg-release-essentials.zip"
   - Extract to `C:\ffmpeg`
   - Search "Environment Variables" in Start menu
   - Under System Variables, find `Path`, click Edit
   - Add `C:\ffmpeg\bin`
   - Click OK, restart PowerShell

   Verify:
   ```
   ffmpeg -version
   ```

3. **Download this repo**

   ```
   git clone https://github.com/gemimakruva/yt-transcribe.git
   cd yt-transcribe
   ```

   Or download as ZIP from the green "Code" button above > Extract.

4. **Install dependencies**

   ```
   pip install -r requirements.txt
   ```

5. **Done!** See [Usage](#usage) below.

</details>

<details>
<summary><strong>Mac (detailed)</strong></summary>

1. **Install Homebrew** (skip if you already have it)

   ```
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install Python** (skip if you already have it)

   ```
   brew install python
   ```

   Verify:
   ```
   python3 --version
   ```

3. **Install FFmpeg**

   ```
   brew install ffmpeg
   ```

   Verify:
   ```
   ffmpeg -version
   ```

4. **Download this repo**

   ```
   git clone https://github.com/gemimakruva/yt-transcribe.git
   cd yt-transcribe
   ```

5. **Install dependencies**

   ```
   pip3 install -r requirements.txt
   ```

6. **Done!** See [Usage](#usage) below.

> **Note:** On Mac, use `python3` and `pip3` instead of `python` and `pip`.

</details>

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
