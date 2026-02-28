---
name: ai-coaching-podcast
description: Daily 25-30 min AI coaching podcast. Combines psychology, goal tracking, conversation analysis, book concepts, and industry news into a spoken deep-dive. Generated as audio via ElevenLabs.
---

# Daily Audio Coaching Podcast

## Overview

Every morning, generate a ~30-minute audio coaching session. The user listens during their commute or exercise. The session is a deep-dive written as a spoken monologue and converted to audio via ElevenLabs.

## Prerequisites

- ElevenLabs API key (set in `ELEVENLABS_API_KEY` env var or config)
- ffmpeg installed (`brew install ffmpeg`)
- Transcript source (e.g., wear-transcribe skill, Omi, or any daily transcript)
- Filled-in reference files (see `references/` folder)

## Voice & Model

Configure in `scripts/config.json`:
- **Voice:** Choose from ElevenLabs voice library
- **Model:** `eleven_multilingual_v2` recommended (most lifelike)
- **Generator script:** `scripts/generate-audio.py`

## The Coaching Team

Each session draws from multiple perspectives:

### The Psychologist
- Draws from: `references/coaching-profile.md` (Triggers / Context sections)
- Understands: attachment patterns, defenses, cognitive distortions, growth areas
- Role: connects today's topic to deep patterns. Challenges surface-level explanations. Validates genuine progress.

### The Coach
- Draws from: `references/coaching-profile.md` (copy from template), `references/goals.md` (copy from template)
- Tracks: your goal pillars with RAG scoring (🟢🟡🔴)
- Role: practical actions, micro-commitments, accountability, progress tracking

### The Industry Researcher
- Sources: news, Slack, industry feeds, competitor updates
- Role: hyper-relevant intelligence filtered through what matters for YOUR work

### The Personal Assistant
- Draws from: calendar, tasks, messages, transcripts
- Role: grounds the session in today's reality — meetings ahead, people to prep for, tasks due

## Data Sync (CRITICAL — do this BEFORE writing the script)

Before generating content, sync ALL available sources:

1. **Transcripts** — yesterday's diarized transcripts (from wear-transcribe or equivalent)
2. **Calendar** — today's and tomorrow's events
3. **Tasks** — overdue, due today, due this week
4. **Messages** — recent WhatsApp, Slack, email highlights
5. **Previous scorecards** — last evening scorecard, last weekly review

Never write a coaching script without fresh data. The power of this system is that it knows what actually happened — generic advice is worthless.

## Script Writing Guide

### Format
- ~6000-7000 words = ~35-42 minutes of spoken audio
- Written as **spoken monologue**, NOT a document
- Direct address: "you", "your"
- Conversational but substantive — not dumbed down, not academic

### Structure (flexible, not rigid)

1. **Opening** (30 sec) — "Good morning. Today I want to talk about..." Ground it in something specific from yesterday.
2. **Conversation Analysis** (5-8 min) — Pick 2-3 moments from yesterday's transcripts. Reframe them. What was really happening beneath the surface? What patterns show up?
3. **Goal Coaching** (5-8 min) — RAG scorecard for each goal pillar. Evidence from yesterday. What to incorporate today. Be specific.
4. **People Prep** (3-5 min) — Who are you meeting today? What's the dynamic? What's the one thing to remember going in?
5. **Book Deep-Dive** (5-8 min) — One concept from your reading list, applied to something that happened yesterday or is coming up today. Not a summary — teach ONE idea deeply with stories and tie it to your specific situation.
6. **Industry Update** (3-5 min) — What happened in your industry that matters. Not a news roundup — filtered through your strategic context.
7. **Micro-commitment** (2 min) — One specific thing to do today. Not "be more productive" — "Before the 10am standup, write down one thing you shipped yesterday and say it first."
8. **Close** (30 sec) — Warm, grounding.

### Tone — Like a Book Chapter
The audio should feel like listening to a chapter from a well-written book. NOT a pep talk. NOT bullet points read aloud.

- **Depth over breadth** — one theme explored richly
- **Real references** — cite psychology research, name frameworks, reference case studies
- **Stories** — other people who faced similar dynamics, historical figures, research subjects
- **Book concepts woven in naturally** — not "as the author says in chapter 4" but the concept applied to a specific situation

### Verification Rules
- **Every person mentioned** must appear in yesterday's transcripts, calendar, or messages
- **Every quote** must be verified against source data
- **Every meeting** must be confirmed on the calendar
- Never fabricate conversations or attribute statements that didn't happen

## Audio Generation

After writing the script, save it to a text file and run:

```bash
python3 scripts/generate-audio.py script.txt [output-name]
```

The script handles:
- Chunking text at 4500 chars (ElevenLabs API limit)
- Generating audio for each chunk
- Concatenating with ffmpeg
- Output as MP3

## Cron Configuration

Example OpenClaw cron (7am daily, weekdays):

```json
{
  "name": "Daily Audio Coaching",
  "schedule": { "kind": "cron", "expr": "0 7 * * 1-5", "tz": "YOUR_TIMEZONE" },
  "payload": {
    "kind": "agentTurn",
    "message": "Read and follow skills/ai-coaching-podcast/SKILL.md",
    "timeoutSeconds": 600
  }
}
```

## Scorecard Format

For evening scorecards (optional companion to the podcast):

```
═══ Evening Scorecard — [DATE] ═══

GOAL 1: [Name] — 🟢/🟡/🔴
• Evidence: [specific thing from today]
• Evidence: [another specific thing]

GOAL 2: [Name] — 🟢/🟡/🔴
• Evidence: ...

═══ Pre-commits for tomorrow ═══
1. [Specific, measurable action]
```

## Topic Selection

Before writing, read `references/topic-log.md` to avoid repetition.

**Rules:**
- Never repeat a framework within 7 days
- Never tell the same story twice in 14 days
- Rotate categories — don't do 3 of the same type in a row
- Book concepts: one per day, applied specifically. Not a summary.
- Log every session after generating

**Pick the topic based on:**
1. What happened yesterday (transcripts are the primary signal)
2. What's coming today (calendar)
3. Where the 90-day plan says you should be this week
4. What hasn't been covered recently (check the log)

## What Makes a GOOD Session

- Opens with something specific from yesterday — a real moment, a real conversation
- Makes you think "how did it know that?" — because it read the transcripts
- Teaches ONE concept deeply, applied to YOUR situation
- Ends with a micro-commitment you can actually do today
- Feels like a friend who knows you well, not a coach reading from a script

## What Makes a BAD Session

- Generic advice that could apply to anyone ("remember to be present today")
- Repeating the same framework from 3 days ago
- Mentioning people or meetings that didn't happen (hallucination)
- Reading a news roundup with no connection to your work
- Bullet points read aloud instead of a flowing narrative
- Motivational pep talk energy ("You've got this!")

## On-Demand Evening Sessions

When triggered manually (e.g., "reflect" or "evening podcast"):
- Use the evening scorecard data — don't re-sync everything
- Shorter: 10-15 min (vs 30 min morning)
- Focus on processing the day, not prepping for tomorrow
- More reflective, less prescriptive
- Speed matters — generate quickly, user listens on the way home

## Tracking

### Topic Log (`references/topic-log.md`)
After every session, append a row with date, category, and key topics covered. This prevents repetition and ensures balanced coverage.

### 90-Day Plan (`references/90-day-plan.md`)
Check the current week's targets. The podcast should reference what the user should be practicing THIS week, not generic goals.

## Adaptive Coaching

- If a goal scores 🔴 for 2+ weeks → escalate in next audio, increase focus
- If a goal scores 🟢 for 2+ weeks → de-escalate, shift attention elsewhere
- If user says "less" on any topic → reduce and note the preference
- Vary the structure and format to keep it fresh — not every day needs the same order
