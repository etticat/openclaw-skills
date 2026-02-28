# Setup — Wear Transcribe

## 1. Install dependencies

```bash
# Core
brew install ffmpeg
pip install openai-whisper requests

# Whisper needs PyTorch
pip install torch
```

## 2. Set up Google Drive OAuth (for watch-pull.sh)

ClawHark uploads recordings to Google Drive. This script pulls them down.

### Create a Google Cloud project
1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a new project (or use existing)
3. Enable the **Google Drive API**
4. Go to **Credentials** → Create OAuth 2.0 Client ID
5. Type: **Desktop application**
6. Download the credentials JSON

### Get a refresh token
```bash
# Install oauth helper
pip install google-auth-oauthlib

# Run the OAuth flow
python3 << 'EOF'
from google_auth_oauthlib.flow import InstalledAppFlow

flow = InstalledAppFlow.from_client_secrets_file(
    'path/to/downloaded/credentials.json',
    scopes=['https://www.googleapis.com/auth/drive.file']
)
creds = flow.run_local_server(port=0)

import json
token_data = {
    "client_id": flow.client_config['client_id'],
    "client_secret": flow.client_config['client_secret'],
    "refresh_token": creds.refresh_token
}

with open('drive_refresh_token.json', 'w') as f:
    json.dump(token_data, f, indent=2)

print("✅ Saved to drive_refresh_token.json")
EOF

# Move to secrets
mkdir -p ~/.openclaw/secrets
mv drive_refresh_token.json ~/.openclaw/secrets/
```

## 3. Get an AssemblyAI API key

1. Sign up at [assemblyai.com](https://www.assemblyai.com)
2. Copy your API key from the dashboard
3. Save it:

```bash
echo "your-api-key" > ~/.openclaw/secrets/assemblyai_api_key
```

Or set: `export ASSEMBLYAI_API_KEY=your-key`

## 4. Install ClawHark on your watch

Follow the setup guide at [github.com/etticat/clawhark](https://github.com/etticat/clawhark).

ClawHark records audio on your Wear OS watch and uploads 5-min chunks to Google Drive.

## 5. Create the recordings directory

```bash
mkdir -p ~/.openclaw/workspace/watch-recordings/transcripts
```

## 6. Make scripts executable

```bash
chmod +x scripts/watch-pull.sh
chmod +x scripts/transcribe-pipeline.py
```

## 7. Test it

```bash
# Pull recordings from Drive
./scripts/watch-pull.sh

# Run transcription on a date
python3 scripts/transcribe-pipeline.py 2025-01-15
```

## 8. Set up cron (optional)

```bash
# Pull every 2 hours
openclaw cron create \
  --name "Watch Recorder Pull" \
  --expr "0 */2 * * *" \
  --tz "YOUR_TIMEZONE" \
  --message "Run: bash skills/wear-transcribe/scripts/watch-pull.sh" \
  --timeout 120

# Transcribe daily at 10pm
openclaw cron create \
  --name "Daily Transcription" \
  --expr "0 22 * * *" \
  --tz "YOUR_TIMEZONE" \
  --message "Check for un-transcribed dates in watch-recordings/ and run skills/wear-transcribe/scripts/transcribe-pipeline.py on each" \
  --timeout 3600
```

## Cost

| Component | Cost |
|-----------|------|
| Whisper (local) | Free |
| AssemblyAI | ~$0.37/hr of audio |
| Google Drive API | Free |
| Typical day (2-3hr conversations) | ~$1 |
