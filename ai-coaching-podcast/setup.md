# Setup — AI Coaching Podcast

## 1. Install dependencies

```bash
pip install requests
brew install ffmpeg
```

## 2. Get an ElevenLabs API key

1. Sign up at [elevenlabs.io](https://elevenlabs.io)
2. Go to Profile → API Key
3. Save it:

```bash
mkdir -p ~/.openclaw/secrets
echo "your-api-key-here" > ~/.openclaw/secrets/elevenlabs_api_key
```

Or set as environment variable: `export ELEVENLABS_API_KEY=your-key`

## 3. Choose a voice

Browse voices at [elevenlabs.io/voice-library](https://elevenlabs.io/voice-library). Find one you'd enjoy listening to for 30 minutes daily.

Edit `scripts/config.json`:
```json
{
  "voice_id": "YOUR_VOICE_ID",
  "model_id": "eleven_multilingual_v2"
}
```

**Recommended voices for coaching:**
- George (`JBFqnCBsd6RMkjVDRZzb`) — warm, natural storytelling voice
- Daniel (`onwK4e9ZLuTAKqWW03F9`) — authoritative, clear
- Rachel (`21m00Tcm4TlvDq8ikWAM`) — calm, clear

## 4. Fill in your reference files

This is the most important step. The coaching quality is directly proportional to how much context you provide.

### Required:
1. **`references/coaching-profile.md`** — Copy the template. Fill in your patterns, triggers, strengths, context. Be honest — the AI is your coach, not your interviewer.

2. **`references/goals.md`** — Define 3-7 pillars with specific scoring criteria. Start with 3 — you can always add more.

### Optional but recommended:
3. **`references/reading-list.md`** — Books whose concepts you want woven into sessions.

## 5. Set up transcript source

The coaching system is most powerful when it has access to your conversations. Options:

- **[ClawHark](https://github.com/etticat/clawhark) + wear-transcribe skill** — always-on recording from your watch
- **Omi** — AI wearable companion
- **Scribbl / Otter.ai** — meeting transcripts
- **Manual** — paste conversation summaries into a daily file

The SKILL.md expects transcripts at a known path. Update the data sync section to match your setup.

## 6. Set up the cron

In OpenClaw, create a cron job:

```bash
openclaw cron create \
  --name "Daily Audio Coaching" \
  --expr "0 7 * * 1-5" \
  --tz "YOUR_TIMEZONE" \
  --message "Read and follow skills/ai-coaching-podcast/SKILL.md" \
  --timeout 600
```

Adjust the time and timezone for your commute.

## 7. Test it

```bash
# Create a test script
echo "Good morning. This is a test of your coaching audio system. If you can hear this, everything is working correctly." > /tmp/test-script.txt

# Generate audio
python3 scripts/generate-audio.py /tmp/test-script.txt test-audio
```

You should get an MP3 in `~/.openclaw/workspace/audio-coaching/`.

## Cost

- ElevenLabs: ~$5-11/month for daily 30-min sessions (depends on plan)
- Everything else: free
