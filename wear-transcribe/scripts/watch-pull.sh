#!/bin/bash
# Pull watch recordings from Google Drive and organize by date.
# Downloads all files from the ClawHark/WearRecorder folder, organized into date folders.
# Deletes from Drive after successful download.
#
# Prerequisites:
#   - Google Drive OAuth credentials (see setup.md)
#   - Python 3.9+
#
# Usage: ./watch-pull.sh

set -euo pipefail

# Config — adjust these paths
RECORDINGS_DIR="${WATCH_RECORDINGS_DIR:-$HOME/.openclaw/workspace/watch-recordings}"
CREDENTIALS_FILE="${DRIVE_CREDENTIALS:-$HOME/.openclaw/secrets/drive_refresh_token.json}"
DRIVE_FOLDER_NAME="${DRIVE_FOLDER:-ClawHark}"

echo "=== Watch Recorder Pull — $(date) ==="

if [ ! -f "$CREDENTIALS_FILE" ]; then
    echo "❌ Credentials not found: $CREDENTIALS_FILE"
    echo "   Run setup to configure Google Drive OAuth."
    exit 1
fi

# Get Drive access token
ACCESS_TOKEN=$(python3 << PYEOF
import json, urllib.request, urllib.parse
with open("$CREDENTIALS_FILE") as f:
    d = json.load(f)
data = urllib.parse.urlencode({
    "client_id": d["client_id"],
    "client_secret": d["client_secret"],
    "refresh_token": d["refresh_token"],
    "grant_type": "refresh_token"
}).encode()
r = json.loads(urllib.request.urlopen(
    urllib.request.Request("https://oauth2.googleapis.com/token", data=data)
).read())
print(r["access_token"])
PYEOF
)

# Find the recordings folder on Drive
FOLDER_ID=$(curl -sf -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://www.googleapis.com/drive/v3/files?q=name%3D%27${DRIVE_FOLDER_NAME}%27+and+mimeType%3D%27application%2Fvnd.google-apps.folder%27+and+trashed%3Dfalse&fields=files(id)" \
  | python3 -c "import sys,json; f=json.load(sys.stdin)['files']; print(f[0]['id'] if f else '')")

if [ -z "$FOLDER_ID" ]; then
    echo "No $DRIVE_FOLDER_NAME folder on Drive."
    exit 0
fi

# Download all files, organized by date extracted from filename
python3 << PYEOF
import json, urllib.request, os

token = "$ACCESS_TOKEN"
folder_id = "$FOLDER_ID"
base = os.path.expanduser("$RECORDINGS_DIR")

# List all files (paginated)
all_files = []
page_token = None
while True:
    url = f"https://www.googleapis.com/drive/v3/files?q=%27{folder_id}%27+in+parents+and+trashed%3Dfalse&fields=files(id,name,size),nextPageToken&orderBy=name&pageSize=1000"
    if page_token:
        url += f"&pageToken={page_token}"
    resp = json.loads(urllib.request.urlopen(
        urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    ).read())
    all_files.extend(resp.get("files", []))
    page_token = resp.get("nextPageToken")
    if not page_token:
        break

print(f"Found {len(all_files)} recordings on Drive")

if not all_files:
    exit(0)

downloaded = 0
deleted = 0
for f in all_files:
    name = f["name"]
    # Extract date from filename: chunk_2025-01-13_... → 2025-01-13
    parts = name.split("_")
    date = parts[1] if len(parts) >= 2 else "unknown"

    out_dir = os.path.join(base, date)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, name)

    if os.path.exists(out_path):
        # Already have it — delete from Drive
        try:
            urllib.request.urlopen(urllib.request.Request(
                f"https://www.googleapis.com/drive/v3/files/{f['id']}",
                method="DELETE",
                headers={"Authorization": f"Bearer {token}"}))
            deleted += 1
        except: pass
        continue

    # Download
    try:
        req = urllib.request.Request(
            f"https://www.googleapis.com/drive/v3/files/{f['id']}?alt=media",
            headers={"Authorization": f"Bearer {token}"})
        data = urllib.request.urlopen(req).read()
        with open(out_path, "wb") as fout:
            fout.write(data)
        downloaded += 1
        if downloaded % 10 == 0:
            print(f"  Downloaded {downloaded}...")

        # Delete from Drive after download
        try:
            urllib.request.urlopen(urllib.request.Request(
                f"https://www.googleapis.com/drive/v3/files/{f['id']}",
                method="DELETE",
                headers={"Authorization": f"Bearer {token}"}))
            deleted += 1
        except: pass
    except Exception as e:
        print(f"  Error: {name}: {e}")

print(f"Done. Downloaded {downloaded} new, deleted {deleted} from Drive.")

# Summary by date
for date_dir in sorted(os.listdir(base)):
    dp = os.path.join(base, date_dir)
    if os.path.isdir(dp) and date_dir[0:2] == "20":
        count = len([x for x in os.listdir(dp) if x.endswith((".m4a", ".wav"))])
        if count:
            print(f"  {date_dir}: {count} chunks")
PYEOF
