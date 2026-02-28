# 🎙️ AI Coaching Podcast

**A daily AI-generated coaching podcast that knows what actually happened in your life.**

Not generic motivation. Not "set your intentions." Your AI reads yesterday's conversations, checks your goals, looks at today's calendar — then generates a 30-minute spoken deep-dive you listen to on your commute.

## What it covers

| Section | Time | What happens |
|---------|------|-------------|
| **Conversation analysis** | 5-8 min | Picks 2-3 moments from yesterday. Reframes them. Surfaces the patterns you missed. |
| **Goal coaching** | 5-8 min | 🟢🟡🔴 scorecard for each life pillar. Evidence from yesterday. Specific actions for today. |
| **People prep** | 3-5 min | Who you're meeting today. The dynamics. The one thing to remember going in. |
| **Book deep-dive** | 5-8 min | One concept from your reading list, applied to something that happened yesterday. Not a summary — one idea, taught deeply. |
| **Industry update** | 3-5 min | What happened in your industry that actually matters for your work. |
| **Micro-commitment** | 2 min | One specific thing. Not "be more productive" — "Before the 10am standup, write down one thing you shipped yesterday and say it first." |

## Why audio?

Text coaching gets ignored. I built text-based coaching first — scorecards, reminders, prompts. Engagement: 0%.

Switched to a 30-minute podcast for the commute. Engagement: 100%.

**Build for the medium your user actually consumes.**

## How it works

1. **Sync** — Pull transcripts, calendar, messages, tasks
2. **Write** — AI generates a 6,000-word spoken monologue (book-chapter quality, not bullet points)
3. **Generate** — ElevenLabs converts to audio, chunked at 4,500 chars and concatenated with ffmpeg
4. **Deliver** — Sent via Telegram, WhatsApp, or any channel

## What you need

- [OpenClaw](https://github.com/openclaw/openclaw)
- [ElevenLabs](https://elevenlabs.io) API key (~$5-11/month)
- ffmpeg (`brew install ffmpeg`)
- A transcript source (e.g., [ClawHark](https://github.com/etticat/clawhark) + wear-transcribe, or any daily transcript)

## Setup

See **[setup.md](./setup.md)** for step-by-step instructions.

The most important step is filling in the reference templates — your coaching profile, goal pillars, and reading list. The AI is only as good as the context you give it.

## Files

```
ai-coaching-podcast/
├── SKILL.md                                   # How the AI generates sessions
├── scripts/
│   ├── generate-audio.py                      # ElevenLabs TTS + ffmpeg concat
│   └── config.json                            # Voice and model settings
├── references/
│   ├── coaching-profile-template.md           # Your patterns, triggers, context
│   ├── goals-template.md                      # Goal pillars with 🟢🟡🔴 scoring
│   ├── reading-list-template.md               # Books for daily concept deep-dives
│   ├── 90-day-plan-template.md                # Week-by-week phased coaching plan
│   └── topic-log-template.md                  # Session log — prevents repetition
├── requirements.txt
└── setup.md
```
