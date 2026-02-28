<p align="center">
  <strong>🧠</strong>
</p>

<h1 align="center">OpenClaw Skills</h1>

<p align="center">
  <strong>AI skills that actually change your life.</strong><br>
  Not chatbots. Not wrappers. A system that listens, coaches, and acts.
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License" /></a>
  <a href="https://github.com/openclaw/openclaw"><img src="https://img.shields.io/badge/built_for-OpenClaw-orange.svg" alt="OpenClaw" /></a>
  <a href="https://github.com/etticat/clawhark"><img src="https://img.shields.io/badge/pairs_with-ClawHark-green.svg" alt="ClawHark" /></a>
</p>

---

Five [OpenClaw](https://github.com/openclaw/openclaw) skills, extracted from a real system that runs 24/7. Each one is self-contained and ready to install.

> **The origin story:** I built an AI that records my conversations via my watch, generates a 30-minute coaching podcast every morning, nags me when I'm neglecting friends, mines my day for social media content, and orders my groceries. This repo is that system, open sourced and genericized.

## Skills

| | Skill | What it does | Needs |
|---|-------|-------------|-------|
| 🎙️ | **[ai-coaching-podcast](./ai-coaching-podcast/)** | Daily 30-min AI coaching podcast. Analyzes yesterday's conversations, tracks your goals (🟢🟡🔴), preps you for key meetings, deep-dives into books you're reading, and delivers it as audio you listen to on your commute. | ElevenLabs API, ffmpeg |
| ⌚ | **[wear-transcribe](./wear-transcribe/)** | Turns watch recordings into speaker-diarized transcripts. Local Whisper filters out silence first (saves 60-80% on API costs), then AssemblyAI handles the real transcription. | Whisper, AssemblyAI API |
| 👥 | **[relationship-outreach](./relationship-outreach/)** | Scans WhatsApp, Slack, email, calendar, and transcripts. Finds neglected friends, unreturned messages, and owed follow-ups. Suggests 1-3 people to reach out to with genuine openers. Escalates if you ignore it. | Communication tools |
| 📱 | **[social-media-capture](./social-media-capture/)** | Mines your transcripts, messages, and meetings for postable insights. Matches your voice. Presents drafts for approval — never auto-posts. | Transcript source |
| 🛒 | **[grocery-autopilot](./grocery-autopilot/)** | Automated weekly grocery ordering via browser. Logs in, books a slot, fills the basket from your list, checks out. You configure it once. | Browser automation |

## How they connect

| Layer | What | Skill |
|-------|------|-------|
| **Capture** | Watch records all day, uploads to Drive | [ClawHark](https://github.com/etticat/clawhark) |
| **Transcribe** | Whisper filters → AssemblyAI diarizes | wear-transcribe |
| **Coach** | Morning podcast from your real data | ai-coaching-podcast |
| **Connect** | Find neglected relationships | relationship-outreach |
| **Create** | Mine conversations for content | social-media-capture |
| **Automate** | Weekly groceries on autopilot | grocery-autopilot |

Each skill works independently. Use one, use all five, or mix with your own.

## Quick start

```bash
# Clone
git clone https://github.com/etticat/openclaw-skills.git

# Copy the skills you want into your OpenClaw workspace
cp -r openclaw-skills/ai-coaching-podcast ~/.openclaw/workspace/skills/
cp -r openclaw-skills/wear-transcribe ~/.openclaw/workspace/skills/

# Follow each skill's setup.md
```

**Prerequisites:** [OpenClaw](https://github.com/openclaw/openclaw) · Python 3.9+ · ffmpeg

## Why audio?

Text coaching gets ignored. Push notifications get swiped. Scorecards get skimmed.

A 30-minute podcast during your commute? You can't NOT listen — you're commuting anyway.

These skills were built around that discovery: **the medium matters more than the message.** Build for how people actually consume, not how they say they will.

## Contributing

Found a bug? Want to add a store to grocery-autopilot? PRs welcome.

## License

MIT
