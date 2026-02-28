# Setup — Relationship Outreach

## 1. Set up your contact list

Copy `references/contacts-template.json` → `references/contacts.json`

Add your people. Start with 5-10 — the people you care about but tend to neglect. Be honest about the dynamics.

**Categories:**
- `partner` — gets a special daily check
- `close_friend` — flagged after 14 days of silence
- `family` — flagged after 21 days
- `colleague` — flagged after 14 days if you work closely
- `acquaintance` — no automatic flagging

## 2. Configure communication channels

The skill scans multiple channels. Configure whichever you use:

### WhatsApp (via wacli)
```bash
brew install steipete/tap/wacli
wacli auth  # QR code login
```

### Slack
Set up the Slack API script or use OpenClaw's built-in Slack skill.

### Gmail (via gog CLI)
```bash
gog auth --account your@email.com
```

### Calendar (via gog CLI)
```bash
gog auth --account your@email.com
```

### Conversation Transcripts
If using the `wear-transcribe` skill, transcripts are automatically available. Otherwise, configure your transcript source path in the SKILL.md.

## 3. Set up the cron

```bash
openclaw cron create \
  --name "Daily Outreach Coach" \
  --expr "0 9 * * 1-5" \
  --tz "YOUR_TIMEZONE" \
  --message "Read and follow skills/relationship-outreach/SKILL.md" \
  --timeout 300
```

## 4. The first week

The first few days, the skill will be noisy as it catches up on who's been neglected. After a week of data, it stabilizes and becomes genuinely useful.

**The most important thing:** actually DO the outreach it suggests. If you ignore it for 3 days, it'll escalate. That's by design.

## Cost

No additional API costs. Uses your existing OpenClaw AI and configured communication tools.
