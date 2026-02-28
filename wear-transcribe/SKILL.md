---
name: wear-transcribe
description: Full pipeline to turn Wear OS watch recordings into AI-ready diarized transcripts. Local Whisper first pass filters silence, then AssemblyAI provides speaker-diarized transcription. Works with ClawHark.
---

# Wear Transcribe

## Overview

Pipeline to turn always-on watch recordings into speaker-diarized, AI-ready transcripts.

Designed for [ClawHark](https://github.com/etticat/clawhark) but works with any chunked audio recordings organized by date.

## Pipeline Phases

### Phase 1: Pull recordings from Google Drive
```bash
scripts/watch-pull.sh
```
Downloads recordings from the ClawHark Google Drive folder, organizes by date, deletes from Drive after download.

### Phase 2: Whisper local first pass
```bash
python3 scripts/transcribe-pipeline.py YYYY-MM-DD --phase 1
```
Fast local pass with Whisper `base` model. Detects content vs silence. This is crucial — filters out 60-80% of chunks before expensive API calls.

### Phase 3: Segment into conversations
```bash
python3 scripts/transcribe-pipeline.py YYYY-MM-DD --phase 2
```
Groups content chunks into conversations by time proximity (>10 min gap = new conversation).

### Phase 4: Concatenate conversation audio
```bash
python3 scripts/transcribe-pipeline.py YYYY-MM-DD --phase 3
```
Merges related chunks into single conversation audio files using ffmpeg.

### Phase 5: Full diarized transcription
```bash
python3 scripts/transcribe-pipeline.py YYYY-MM-DD --phase 4
```
Sends conversation audio to AssemblyAI Universal-3 for speaker-diarized transcription. Output: markdown transcript with speaker labels and timestamps.

### Run all phases at once
```bash
python3 scripts/transcribe-pipeline.py YYYY-MM-DD
```

## Directory Structure

```
watch-recordings/
├── 2025-01-15/
│   ├── chunk_2025-01-15_09-15-30.m4a
│   ├── chunk_2025-01-15_09-20-30.m4a
│   ├── ...
│   ├── phase1_whisper.json          # Whisper results
│   ├── phase2_segments.json         # Conversation groupings
│   └── conversations/               # Concatenated audio
│       ├── conversation_1_2025-01-15T09-15.m4a
│       └── conversation_2_2025-01-15T14-30.m4a
└── transcripts/
    └── 2025-01-15-diarized.md       # Final transcript
```

## Output Format

```markdown
# Watch Recordings — 2025-01-15

## Conversation 1 — 2025-01-15 09:15 (23.5 min)

[00:00] Speaker A: So I was thinking about the deployment...
[00:15] Speaker B: Yeah, we should probably...
[02:30] Speaker A: Right, and the other thing is...

---

## Conversation 2 — 2025-01-15 14:30 (8.2 min)
...
```

## Cron Configuration

Pull recordings on every heartbeat or on a schedule:

```json
{
  "name": "Watch Recorder Pull",
  "schedule": { "kind": "cron", "expr": "0 */2 * * *", "tz": "YOUR_TIMEZONE" },
  "payload": {
    "kind": "agentTurn",
    "message": "Run scripts/watch-pull.sh to pull new recordings. Then check for un-transcribed dates and run the full pipeline on any that need it.",
    "timeoutSeconds": 3600
  }
}
```

## When to Run

- **Pull:** Every 2 hours or on heartbeat — lightweight, just downloads
- **Transcribe:** Once daily, after work hours — heavy, takes ~1hr for a full day
- **Skip overnight:** Don't start transcription during quiet hours (23:00–08:00)

## Cost

- Whisper local pass: free (runs on your machine)
- AssemblyAI: ~$0.37/hr of audio. A typical day with 2-3 hours of conversation content costs ~$1
- Google Drive API: free
