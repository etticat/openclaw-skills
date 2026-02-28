# Setup — Social Media Capture

## 1. Set up a transcript source

The skill needs access to your real conversations. The richer the source, the better the extractions.

**Best:** [ClawHark](https://github.com/etticat/clawhark) + [wear-transcribe](../wear-transcribe/) — always-on recording from your watch, capturing hallway conversations, meeting side-comments, and things you say but never write down.

**Good:** Meeting transcripts (Scribbl, Otter.ai), Slack messages, WhatsApp messages.

**Minimum:** Any daily notes or logs where you record your thinking.

## 2. Fill in your voice guide

Copy `references/voice-guide-template.md` to `references/voice-guide.md` and fill it in.

**How to do this well:**
1. Open your last 20 social media posts
2. Notice your patterns: sentence length, word choice, what you say vs don't say
3. Identify 3-5 "signature moves" — recurring patterns in how you write
4. Be specific with examples — paste real posts
5. List your anti-patterns — what you NEVER want to sound like

The voice guide is your starting point. The learned preferences file (next step) refines it over time.

## 3. Create the learned preferences file

Copy `references/learned-preferences-template.md` to `references/learned-preferences.md`.

Start it empty. The skill fills it in automatically based on your approvals, rejections, edits, and feedback. After a few weeks, it knows exactly what you'll approve.

## 4. Set up the cron (optional)

```bash
openclaw cron create \
  --name "Social Media Capture" \
  --expr "0 20 * * *" \
  --tz "YOUR_TIMEZONE" \
  --message "Read and follow skills/social-media-capture/SKILL.md" \
  --timeout 300
```

Or run on-demand: just ask your AI "mine today for social media content."

## 5. Interact with the drafts

Each draft comes with buttons: `✅ Approve` `❌ Decline` `✏️ Edit` `💬 Feedback`

Use them. Every interaction teaches the skill what you want. The first few sessions will be noisy — it doesn't know your preferences yet. By week 2, it's sharp.

## Cost

Free. No additional API costs beyond your existing OpenClaw setup.
