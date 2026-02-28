---
name: relationship-outreach
description: Daily relationship outreach coach. Scans WhatsApp, Slack, email, calendar, and conversation transcripts to recommend who to reach out to today and why. Focuses on genuine human connection, not transactional check-ins.
---

# Relationship Outreach

Daily morning skill that identifies who you should reach out to today, with specific openers and context. Scans all your communication channels to find who's been neglected, who reached out without a reply, and who's going through something you should acknowledge.

## Philosophy

**This is not task management. This is relationship building.**

Most people default to transactional communication — logistics with partners, work updates with colleagues, silence with friends. This skill shifts you toward genuine curiosity about other people's experiences.

Key principles:
- **Center THEIR experience**, not your needs
- **Low ego** — don't approach people to "manage" them
- **Curiosity over strategy** — "What is this person going through?" not "How do I handle this person?"
- **One meaningful interaction > ten shallow ones**
- **Notice who's reaching out to YOU that you haven't responded to**

## Data Sources

### 1. Contact List
**Location:** `references/contacts.json`

A JSON file tracking your relationships:

```json
[
  {
    "name": "Alex",
    "category": "close_friend",
    "channels": {
      "whatsapp": "+1...",
      "slack": "@alex",
      "email": "alex@example.com"
    },
    "last_contact_date": "2025-01-01",
    "last_topic": "Talked about his new job",
    "follow_ups_owed": ["Send that article about startups"],
    "what_they_care_about": "Rock climbing, career change, recently got a dog",
    "dynamic": "Easy, warm. They tend to reach out first. Could be more reciprocal.",
    "health": "🟢"
  }
]
```

### 2. Communication Channels

**WhatsApp** — check recent messages with each contact:
```bash
wacli messages list <JID> --limit 10
```

**Slack** — check DMs for work contacts:
```bash
# Search for recent messages from/to a person
slack_api search.messages "from:@name after:YYYY-MM-DD"
```

**Email** — check Gmail for recent correspondence:
```bash
gog --account your@email.com gmail search "from:person OR to:person" --max 5
```

**Calendar** — who will you see today?
```bash
gog --account your@email.com calendar events primary --from TODAY --to TOMORROW
```

**Conversation Transcripts** — from ClawHark/wear-transcribe or any transcript source:
- Check yesterday's transcripts for in-person interactions
- Look for mentions of people, promises made, follow-ups discussed

### 3. Coaching Profile (optional)
If using the ai-coaching-podcast skill, reference the coaching profile for:
- Relationship goals and patterns
- Communication tendencies
- People dynamics and challenges

## Selection Algorithm

### Priority 1: Urgent 🔴
- Someone who reached out and got **no response** from you
- Someone going through something hard (visible from transcripts/messages)
- Your partner/spouse — ALWAYS check if there's something present and specific to do today
- Contacts with health: 🔴

### Priority 2: Overdue 🟡
- Follow-ups you owe (promises, questions you said you'd answer)
- People you haven't talked to in 2+ weeks despite being close
- Contacts with health: 🟡

### Priority 3: Maintenance 🟢
- People the relationship is good with but could deepen
- Friends you haven't connected with in a while
- Family members

### Priority 4: New
- New colleagues who might feel unseen
- People you've been introduced to but haven't followed up with

## Output Format

Pick **1-3 people** (not more — quality over quantity). For each:

```
━━━ [Person Name] ━━━
Why now: [Specific reason — they reached out, something happened, overdue]
What they care about: [From CRM / recent interactions]
Last contact: [Date and what you talked about]
Suggested opener: [A specific, human, curious message]
Channel: [WhatsApp / Slack / in-person / call]
Don't: [What to avoid — e.g., "Don't make it about work"]
━━━
```

### Partner/Spouse Check (if configured)
```
━━━ Partner Check ━━━
Yesterday: [What happened between you — from messages/transcripts]
Today: [One specific, small thing you can do that ISN'T logistics]
━━━
```

## Opener Examples

### Good (curious, low-ego)
- "Hey, how are you settling into the new role? Genuinely curious."
- "I've been meaning to ask — how's [personal thing they mentioned] going?"
- "I realized I never asked you about [something]. What's your take?"
- "Just thinking of you. How are things?"
- "Saw [thing relevant to them] and thought of you"

### Bad (transactional, ego-driven)
- "Just wanted to check in" ← vague, no curiosity
- "How's the project going?" ← work-only
- "I wanted to make sure you know I value you" ← performative
- "Let's catch up" ← empty, puts burden on them
- "Long time no speak!" ← guilt-tripping

## Anti-Patterns to Watch

1. **The "I'll do it tomorrow" loop** — if the same person shows up 3 days in a row without action, escalate
2. **Avoidance of difficult relationships** — if you keep picking easy people, name it
3. **Work-framing everything** — if every reach-out becomes a work conversation, name it
4. **Grand gestures over daily presence** — one text asking how someone's doing > planning an elaborate dinner

## CRM Auto-Update

After each daily run, the skill should:
- Update `last_contact_date` for anyone you interacted with yesterday
- Update `last_topic` with what was discussed
- Flag any contacts with staleness > 14 days
- Note any `follow_ups_owed` from conversations
- Recalculate `health` based on staleness and interaction quality

## Cron Configuration

```json
{
  "name": "Daily Outreach Coach",
  "schedule": { "kind": "cron", "expr": "0 9 * * 1-5", "tz": "YOUR_TIMEZONE" },
  "payload": {
    "kind": "agentTurn",
    "message": "Read and follow skills/relationship-outreach/SKILL.md. Scan all channels and recommend who to reach out to today.",
    "timeoutSeconds": 300
  }
}
```

## Integration with Other Skills

- **wear-transcribe** — provides conversation transcripts showing who you talked to in person
- **ai-coaching-podcast** — the morning coaching session can reference outreach recommendations
- **social-media-capture** — if you're engaging with someone's content online, note it as a touchpoint
