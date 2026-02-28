# 👥 Relationship Outreach

**Your AI tells you who to reach out to today — and why.**

Not a reminder app. Not a CRM. A relationship coach that scans your actual communications across WhatsApp, Slack, email, calendar, and conversation transcripts — then tells you who's been neglected, who reached out without a reply, and exactly what to say.

## The problem

You have friends you care about. You don't reach out enough. Not because you don't care — because you're busy, and "I should message Alex" never survives your todo list.

Meanwhile, people reach out to YOU and you forget to respond. You promise follow-ups and never deliver. Weeks pass. The relationship quietly decays.

## What it does

Every morning, your AI:

1. **Scans all channels** — WhatsApp, Slack, email, calendar, conversation transcripts
2. **Identifies 1-3 people** who need attention — unreturned messages, overdue follow-ups, friends gone quiet
3. **Suggests genuine openers** — not "let's catch up" but "how's the new job going?"
4. **Updates the CRM** — tracks interactions, flags staleness, notes follow-ups owed
5. **Escalates** — if the same person shows up 3 days in a row without action, it gets louder

## Example output

```
━━━ Alex ━━━
Why now: He messaged you 4 days ago. You never replied.
What he cares about: Training for a marathon, thinking about changing careers
Opener: "How's the marathon training going? You must be getting close."
Channel: WhatsApp
Don't: Don't make it about work.
━━━

━━━ Partner Check ━━━
Yesterday: Quick chat about weekend plans. Nothing deep.
Today: They mentioned a job interview last week — ask how it went.
━━━
```

## What makes this different

| Feature | Reminder apps | This skill |
|---------|--------------|------------|
| Knows who you actually talked to | ❌ | ✅ Scans real messages |
| Knows who you spoke to in person | ❌ | ✅ Reads conversation transcripts |
| Suggests what to say | ❌ | ✅ Context-aware openers |
| Detects avoidance patterns | ❌ | ✅ Calls you out |
| Partner/spouse daily check | ❌ | ✅ Meaningful daily prompt |

## What you need

- [OpenClaw](https://github.com/openclaw/openclaw)
- At least one communication channel configured:
  - WhatsApp (via [wacli](https://github.com/niclas-nicolo/wacli))
  - Slack
  - Gmail / Calendar (via [gog](https://github.com/alexferl/gog))
- Optionally: [ClawHark](https://github.com/etticat/clawhark) + wear-transcribe for in-person conversation awareness

## Setup

See **[setup.md](./setup.md)**. Start with 5-10 contacts — the people you care about but tend to neglect. Be honest about the dynamics.

The first few days will be noisy as it catches up on who's been neglected. After a week, it stabilizes and becomes genuinely useful.

**The most important thing:** actually DO the outreach it suggests.
