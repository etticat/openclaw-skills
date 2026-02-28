#!/usr/bin/env python3
"""
Generate coaching audio via ElevenLabs TTS.

Handles long scripts by chunking at paragraph boundaries (4500 char limit per request),
generating audio for each chunk, and concatenating with ffmpeg.

Usage:
    python3 generate-audio.py <script.txt> [output-name]
    
Environment:
    ELEVENLABS_API_KEY  — your ElevenLabs API key
    
Config:
    Edit config.json in this directory for voice settings.
"""

import os
import sys
import json
import requests
import subprocess
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent
CONFIG_FILE = SCRIPT_DIR / "config.json"

# Default config (overridden by config.json)
DEFAULT_CONFIG = {
    "voice_id": "JBFqnCBsd6RMkjVDRZzb",  # Default voice - change to your preferred voice
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {
        "stability": 0.65,
        "similarity_boost": 0.75,
        "style": 0.35,
        "use_speaker_boost": True
    },
    "output_dir": "~/.openclaw/workspace/audio-coaching",
    "max_chars_per_chunk": 4500
}


def load_config():
    """Load config from config.json, falling back to defaults."""
    config = DEFAULT_CONFIG.copy()
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            user_config = json.load(f)
            config.update(user_config)
    return config


def get_api_key():
    """Get ElevenLabs API key from environment."""
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        # Try reading from OpenClaw secrets
        secret_path = Path("~/.openclaw/secrets/elevenlabs_api_key").expanduser()
        if secret_path.exists():
            key = secret_path.read_text().strip()
    if not key:
        print("❌ Set ELEVENLABS_API_KEY or create ~/.openclaw/secrets/elevenlabs_api_key")
        sys.exit(1)
    return key


def generate_chunk(text: str, api_key: str, config: dict, output_path: Path) -> bool:
    """Generate audio from a single text chunk."""
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{config['voice_id']}"
    
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }
    
    data = {
        "text": text,
        "model_id": config["model_id"],
        "voice_settings": config["voice_settings"]
    }
    
    response = requests.post(url, json=data, headers=headers, timeout=300)
    
    if response.status_code == 200:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'wb') as f:
            f.write(response.content)
        return True
    else:
        print(f"❌ ElevenLabs error {response.status_code}: {response.text[:300]}")
        return False


def split_text(text: str, max_chars: int) -> list[str]:
    """Split text into chunks at paragraph boundaries, respecting max_chars."""
    paragraphs = text.split('\n\n')
    chunks = []
    current = ""
    
    for para in paragraphs:
        if len(current) + len(para) + 2 > max_chars:
            if current:
                chunks.append(current.strip())
            current = para
        else:
            current += "\n\n" + para
    
    if current.strip():
        chunks.append(current.strip())
    
    return chunks


def concatenate_audio(chunk_files: list[Path], output_path: Path) -> bool:
    """Concatenate MP3 files using ffmpeg."""
    list_file = output_path.parent / "_concat_list.txt"
    with open(list_file, 'w') as f:
        for cf in chunk_files:
            f.write(f"file '{cf}'\n")
    
    result = subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(list_file),
         "-c", "copy", str(output_path)],
        capture_output=True, text=True
    )
    
    list_file.unlink(missing_ok=True)
    return result.returncode == 0


def main():
    if len(sys.argv) < 2:
        print("Usage: generate-audio.py <script.txt> [output-name]")
        print("\nGenerates coaching audio from a text script via ElevenLabs.")
        print("Set ELEVENLABS_API_KEY environment variable.")
        sys.exit(1)
    
    config = load_config()
    api_key = get_api_key()
    
    # Read script
    text_file = Path(sys.argv[1])
    if not text_file.exists():
        print(f"❌ File not found: {text_file}")
        sys.exit(1)
    
    text = text_file.read_text()
    print(f"📝 Script: {len(text)} chars (~{len(text.split())} words, ~{len(text.split()) // 150} min audio)")
    
    # Output path
    output_dir = Path(config["output_dir"]).expanduser()
    today = datetime.now().strftime("%Y-%m-%d")
    output_name = sys.argv[2] if len(sys.argv) > 2 else f"coaching-{today}"
    output_path = output_dir / f"{output_name}.mp3"
    
    max_chars = config["max_chars_per_chunk"]
    
    if len(text) <= max_chars:
        # Single chunk
        print("🎙️ Generating audio...")
        if generate_chunk(text, api_key, config, output_path):
            size_mb = output_path.stat().st_size / (1024 * 1024)
            print(f"✅ Done: {output_path} ({size_mb:.1f} MB)")
        else:
            sys.exit(1)
    else:
        # Multi-chunk
        chunks = split_text(text, max_chars)
        print(f"🎙️ Generating {len(chunks)} chunks...")
        
        chunk_files = []
        for i, chunk in enumerate(chunks):
            print(f"  [{i+1}/{len(chunks)}] {len(chunk)} chars...", end=" ", flush=True)
            chunk_path = output_dir / f"_chunk_{i:03d}.mp3"
            if generate_chunk(chunk, api_key, config, chunk_path):
                chunk_files.append(chunk_path)
                print("✅")
            else:
                print("❌")
                for f in chunk_files:
                    f.unlink(missing_ok=True)
                sys.exit(1)
        
        # Concatenate
        print("🔗 Concatenating...")
        if concatenate_audio(chunk_files, output_path):
            size_mb = output_path.stat().st_size / (1024 * 1024)
            print(f"✅ Done: {output_path} ({size_mb:.1f} MB)")
        else:
            print("❌ ffmpeg concatenation failed")
            sys.exit(1)
        
        # Clean up chunks
        for f in chunk_files:
            f.unlink(missing_ok=True)
    
    print(f"\n🎧 Audio ready: {output_path}")


if __name__ == "__main__":
    main()
