---
name: social-media-capture
description: Extracts YOUR real opinions from conversations, meetings, and messages — then drafts social media posts in your voice. Not AI slop. Your actual thinking, captured before you forget it. Learns your preferences over time from approval, rejection, and feedback.
---

# Social Media Capture

## Philosophy

**AI-generated social media content is slop.** Everyone knows it. The posts are generic, the takes are lukewarm, the voice is "helpful assistant."

This skill does something different: it listens to what you ACTUALLY think.

You have opinions all day — in meetings, in Slack, in conversations with your team. Things you'd never think to post because you're busy building. By the end of the day, those insights are gone.

This skill captures them. It reads your transcripts, messages, and meetings — finds the moments where you said something worth sharing — and drafts posts in YOUR voice, not AI voice.

**The output is your opinions, extracted. Not generated. Extracted.**

Every draft is presented with approve/decline buttons. You control what goes out. Over time, the skill learns what you care about, what tone works, and what you reject — building an evolving profile that gets sharper with every interaction.

## Data Sources

The skill mines YOUR real communications. The richer the data, the better the extractions.

### Primary: Conversation Transcripts
- **[ClawHark](https://github.com/etticat/clawhark) + wear-transcribe** — always-on recording from your watch, diarized with speaker labels. This is the richest source: captures hallway conversations, meeting side-comments, and the things you say out loud but never write down.
- **Meeting transcripts** — from Scribbl, Otter.ai, or any recorder
- **Voice memos** — any transcribed audio

### Secondary: Written Communication
- **Slack** — technical discussions, knowledge-share channels, debates
- **WhatsApp/Signal** — conversations with smart people
- **Email** — threads where you articulated something well

### Tertiary: Work Context
- **Calendar** — what meetings happened, what was discussed
- **Tasks/Projects** — what you shipped, what you learned building it
- **Industry news** — your REACTION to it, not the news itself

## What to Extract

### Look for:
- Moments where you explained something clearly to a colleague
- Opinions you expressed with conviction in a meeting
- Contrarian takes you made during a discussion
- "I tried X and here's what happened" stories from your work
- Analogies or reframes you used to make a point
- Patterns you noticed across multiple conversations
- Reactions to industry news that differ from consensus
- Things you said in a meeting that made people go "huh, good point"

### Never extract:
- Private conversations — never quote or attribute
- Company secrets, proprietary information, or unreleased plans
- Personal/family/health/finance details
- Anything that could identify colleagues without their consent
- Generic observations anyone could make — only YOUR unique perspective

### Transform, don't quote
If you said something insightful in a private conversation, transform it into a standalone take. Never attribute. "I told my team X" → just state the insight as your opinion.

## Voice Profile

### Initial Setup
Read `references/voice-guide.md` for the user's baseline style. This includes:
- Sentence length, word choice, punctuation patterns
- Signature moves (reframes, deflations, dry observations, etc.)
- Topics they post about vs. topics they avoid
- Anti-patterns (what they NEVER want to sound like)

### Evolving Profile
Read `references/learned-preferences.md` before every session. This file is updated automatically based on:
- **Approved posts** — what topics, angles, and tones get approved
- **Rejected posts** — what the user consistently declines (topics, framing, length)
- **Feedback** — specific notes the user gives ("too long", "not my voice", "love this angle")
- **Edits** — when the user rewrites a draft, the delta shows what they changed and why

After each session, append observations to `references/learned-preferences.md`:
```
## Session [DATE]
- Approved: [N] posts — topics: [X, Y]
- Rejected: [N] posts — reasons: [too generic, wrong tone, not my opinion]
- Feedback received: "[exact quote]"
- Pattern: [what you learned about their preferences]
```

Over time this builds a detailed model of what the user actually wants to post about, how they want to sound, and what they consider slop.

## Output Format

Present each draft as a message with inline buttons for quick action:

```
━━━ Draft [N] ━━━
Platform: Twitter / LinkedIn / Both
Source: [which transcript/meeting/conversation this came from]

[The actual post text, ready to copy-paste]

[✅ Approve] [❌ Decline] [✏️ Edit] [💬 Feedback]
━━━
```

### Button Actions
- **✅ Approve** — post is good to go. Log approval in learned-preferences.
- **❌ Decline** — not this one. Log rejection with auto-detected reason (topic? tone? too generic?). Ask briefly why if pattern isn't clear.
- **✏️ Edit** — user wants to rework it. Present the text for editing. Log the delta between original and edited version.
- **💬 Feedback** — user has specific notes. Log verbatim in learned-preferences.

### Quality Bar
- Present 3-7 drafts per session. Never more than 10.
- **Quality over quantity** — 2 great posts > 7 mediocre ones.
- **Skip days with nothing worth posting.** Forced content = slop. The whole point is to avoid slop.
- Every draft must contain a genuine opinion the user actually expressed. If you can't trace it back to something they said, don't draft it.

## The Anti-Slop Test

Before presenting any draft, ask:

1. **Did the user actually say/think this?** — can you point to the specific transcript/message where this opinion came from?
2. **Would they recognize this as their own opinion?** — or does it read like generic AI advice?
3. **Does it match their voice?** — sentence length, word choice, energy level?
4. **Would they be embarrassed if a colleague saw this?** — if yes, don't draft it.

If any answer is wrong, discard the draft.

## Cron Configuration

```json
{
  "name": "Social Media Capture",
  "schedule": { "kind": "cron", "expr": "0 20 * * *", "tz": "YOUR_TIMEZONE" },
  "payload": {
    "kind": "agentTurn",
    "message": "Read and follow skills/social-media-capture/SKILL.md. Mine today's sources and present draft posts.",
    "timeoutSeconds": 300
  }
}
```

## Important

- **NEVER post without explicit user approval.** Every post needs a button press.
- **NEVER use real names** from private conversations.
- **This is extraction, not generation.** The user's opinions, not AI opinions.
- **Learn continuously.** Every approval, rejection, and piece of feedback makes the next session better.
