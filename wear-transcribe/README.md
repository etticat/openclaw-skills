# ⌚ Wear Transcribe

**Turn always-on watch recordings into speaker-diarized transcripts.**

Your watch records all day. This pipeline turns those recordings into clean, timestamped, speaker-labeled transcripts that other skills can read — coaching, content mining, relationship tracking.

Designed for [ClawHark](https://github.com/etticat/clawhark), works with any chunked audio recordings.

## The pipeline

| Phase | What happens | Cost |
|-------|-------------|------|
| **Pull** | Download recordings from Google Drive, organize by date | Free |
| **Filter** | Whisper `base` model detects speech vs silence | Free (local) |
| **Segment** | Group chunks into conversations (>10 min gap = new conversation) | Free |
| **Concatenate** | Merge related chunks into conversation audio files | Free |
| **Diarize** | AssemblyAI Universal-3 transcription with speaker labels | ~$0.37/hr |

## Why Whisper first?

A full day of recording = 200+ audio chunks. Most are silence, background noise, or fragments.

The local Whisper pass runs in seconds per chunk and filters out 60-80% before the expensive diarization step.

| | Without Whisper | With Whisper |
|---|---|---|
| **Chunks sent to API** | 200+ | 40-80 |
| **Daily cost** | ~$5 | ~$1 |
| **Monthly cost** | ~$150 | ~$30 |

## Output

```markdown
# Watch Recordings — 2025-01-15

## Conversation 1 — 09:15 (23 min)

[00:00] Speaker A: So I was thinking about the deployment...
[00:15] Speaker B: Yeah, we should probably...
[02:30] Speaker A: Right, and the other thing is...

---

## Conversation 2 — 14:30 (8 min)
...
```

These transcripts feed directly into:
- **ai-coaching-podcast** — analyzes your conversations for the morning session
- **social-media-capture** — mines conversations for postable insights
- **relationship-outreach** — knows who you spoke to in person

## Quick start

```bash
# Install
pip install openai-whisper requests torch
brew install ffmpeg

# Pull recordings from Drive
./scripts/watch-pull.sh

# Transcribe a date (all phases)
python3 scripts/transcribe-pipeline.py 2025-01-15

# Or run individual phases
python3 scripts/transcribe-pipeline.py 2025-01-15 --phase 1  # Whisper only
python3 scripts/transcribe-pipeline.py 2025-01-15 --phase 4  # Diarize only
```

## What you need

- Python 3.9+ · ffmpeg
- [ClawHark](https://github.com/etticat/clawhark) on a Wear OS watch (or any chunked audio source)
- Google Drive OAuth credentials (for the pull script)
- [AssemblyAI](https://www.assemblyai.com) API key (for diarization)

See **[setup.md](./setup.md)** for full installation guide.
