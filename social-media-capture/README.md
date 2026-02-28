# 📱 Social Media Capture

**Your opinions, extracted from your actual conversations. Not AI slop.**

You have insights all day — in meetings, in Slack, in hallway conversations. Things you'd never think to post because you're busy building. By the end of the day, they're gone.

This [OpenClaw](https://github.com/openclaw/openclaw) skill captures them. It reads your transcripts (from [ClawHark](https://github.com/etticat/clawhark) + wear-transcribe, or any source), messages, and meetings — finds the moments where you said something worth sharing — and drafts posts in your voice.

**The difference:** AI social media tools generate content. This skill extracts YOUR real opinions from things you actually said. If it can't trace a draft back to something you expressed, it doesn't draft it.

## How it works

1. **Mine** — reads today's transcripts, Slack, WhatsApp, email, meeting notes
2. **Extract** — finds moments where you had a genuine insight or opinion
3. **Draft** — writes posts matching your voice (sentence length, word choice, signature moves)
4. **Present** — shows each draft with `✅ Approve` `❌ Decline` `✏️ Edit` `💬 Feedback` buttons
5. **Learn** — every approval, rejection, edit, and feedback updates your preference profile

## What makes this different

| | Typical AI content tools | This skill |
|---|---|---|
| **Source** | Generates from prompts | Extracts from your real conversations |
| **Voice** | Generic "helpful AI" tone | Matches YOUR writing style, learns over time |
| **Opinions** | AI opinions (slop) | Your opinions (things you actually said) |
| **Learning** | Static | Evolves from every approve/decline/feedback |
| **Quality control** | "Generate 10 tweets" | Skips days with nothing worth posting |

## The anti-slop test

Every draft must pass:
1. ✅ Did the user actually say or think this? (traceable to a source)
2. ✅ Would they recognize this as their own opinion?
3. ✅ Does it match their voice?
4. ✅ Would they be comfortable if a colleague saw it?

If any answer is no, the draft is discarded.

## Learning over time

The skill maintains two evolving profiles:

**Voice profile** (`references/voice-guide.md`) — your writing style, sentence patterns, signature moves, topics you post about, anti-patterns you hate.

**Learned preferences** (`references/learned-preferences.md`) — built automatically from your interactions:
- Which topics you approve vs. decline
- What tone resonates vs. what feels off
- Specific feedback you've given
- How you edit drafts (the delta reveals what you'd change)

After a few weeks, the skill knows exactly what you'll approve and what you'll reject.

## What you need

- [OpenClaw](https://github.com/openclaw/openclaw)
- A transcript source — ideally [ClawHark](https://github.com/etticat/clawhark) + [wear-transcribe](../wear-transcribe/) for always-on conversation capture
- A filled-in voice guide (`references/voice-guide.md`)

No API keys needed — uses your existing OpenClaw AI.

## Setup

See **[setup.md](./setup.md)**. The key step is filling in the voice guide with your actual writing style — paste real posts as examples. The learned preferences file starts empty and builds itself.
