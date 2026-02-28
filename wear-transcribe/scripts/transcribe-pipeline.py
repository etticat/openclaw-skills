#!/usr/bin/env python3
"""
Wear Audio Recorder Transcription Pipeline

Phase 1: Whisper local fast pass — detect content vs silence
Phase 2: Segment — group chunks into conversations by time gaps
Phase 3: Concatenate — merge related chunks into conversation audio files
Phase 4: Diarize — full speaker-diarized transcription via AssemblyAI

Usage:
    python3 transcribe-pipeline.py <date> [--phase 1|2|3|4|all]
    
    e.g. python3 transcribe-pipeline.py 2025-01-15
         python3 transcribe-pipeline.py 2025-01-15 --phase 1

Environment:
    ASSEMBLYAI_API_KEY   — for phase 4 diarization
    WATCH_RECORDINGS_DIR — override default recordings path
"""

import os
import sys
import json
import re
import subprocess
import time
import requests
from pathlib import Path
from datetime import datetime

# Config
RECORDINGS_DIR = Path(os.environ.get(
    "WATCH_RECORDINGS_DIR",
    os.path.expanduser("~/.openclaw/workspace/watch-recordings")
))


def get_api_key(name, env_var, secret_file):
    """Get API key from environment or secrets file."""
    key = os.environ.get(env_var)
    if not key:
        path = Path(f"~/.openclaw/secrets/{secret_file}").expanduser()
        if path.exists():
            key = path.read_text().strip()
    if not key:
        print(f"❌ Set {env_var} or create ~/.openclaw/secrets/{secret_file}")
        sys.exit(1)
    return key


def get_chunk_time(filename):
    """Extract datetime from chunk filename like chunk_2025-01-10_11-41-27.m4a"""
    m = re.search(r'chunk_(\d{4}-\d{2}-\d{2})_(\d{2})-(\d{2})-(\d{2})', filename)
    if m:
        date_str = m.group(1)
        h, mi, s = m.group(2), m.group(3), m.group(4)
        return datetime.strptime(f"{date_str} {h}:{mi}:{s}", "%Y-%m-%d %H:%M:%S")
    return None


def get_duration(filepath):
    """Get audio duration in seconds via ffprobe."""
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(filepath)],
            capture_output=True, text=True, timeout=10
        )
        return float(result.stdout.strip())
    except:
        return 0


# ═══════════════════════════════════════════
# Phase 1: Local Whisper Pass
# ═══════════════════════════════════════════

def phase1_whisper_pass(date_folder):
    """Fast whisper pass to detect content and get rough transcription."""
    import whisper

    chunks = sorted(date_folder.glob("chunk_*.m4a"))
    if not chunks:
        chunks = sorted(date_folder.glob("chunk_*.wav"))
    if not chunks:
        print(f"No chunks found in {date_folder}")
        return []

    print(f"Phase 1: Whisper pass on {len(chunks)} chunks...")
    model = whisper.load_model("base")  # Fast model for first pass

    results = []
    for i, chunk in enumerate(chunks):
        print(f"  [{i+1}/{len(chunks)}] {chunk.name}...", end=" ", flush=True)

        chunk_time = get_chunk_time(chunk.name)
        duration = get_duration(chunk)

        try:
            result = model.transcribe(str(chunk), language="en", fp16=False)
            text = result["text"].strip()

            # Detect if this is silence/noise or actual content
            has_content = len(text) > 20 and not all(
                w in text.lower() for w in ["thank", "you", "bye"]
            )

            info = {
                "filename": chunk.name,
                "path": str(chunk),
                "time": chunk_time.isoformat() if chunk_time else None,
                "duration": round(duration, 1),
                "has_content": has_content,
                "text_preview": text[:200],
                "text_length": len(text),
            }
            results.append(info)
            status = "✅" if has_content else "⬜ (silence/noise)"
            print(f"{status} ({len(text)} chars)")

        except Exception as e:
            print(f"❌ {e}")
            results.append({
                "filename": chunk.name,
                "path": str(chunk),
                "time": chunk_time.isoformat() if chunk_time else None,
                "duration": round(duration, 1),
                "has_content": False,
                "text_preview": f"[error: {e}]",
                "text_length": 0,
            })

    # Save results
    output = date_folder / "phase1_whisper.json"
    with open(output, "w") as f:
        json.dump(results, f, indent=2)

    content_chunks = [r for r in results if r["has_content"]]
    print(f"\nPhase 1 done: {len(content_chunks)}/{len(results)} chunks have content")
    print(f"Saved: {output}")
    return results


# ═══════════════════════════════════════════
# Phase 2: Segment into Conversations
# ═══════════════════════════════════════════

def phase2_segment(date_folder):
    """Group chunks into conversations based on time gaps."""
    phase1_file = date_folder / "phase1_whisper.json"
    if not phase1_file.exists():
        print("❌ Phase 1 results not found. Run phase 1 first.")
        return []

    with open(phase1_file) as f:
        chunks = json.load(f)

    content_chunks = [c for c in chunks if c["has_content"]]
    if not content_chunks:
        print("No content chunks found.")
        return []

    print(f"Phase 2: Segmenting {len(content_chunks)} content chunks...")

    # Group by time proximity (>10 min gap = new conversation)
    GAP_THRESHOLD = 600  # 10 minutes in seconds
    conversations = []
    current_conv = []

    for chunk in content_chunks:
        chunk_time = datetime.fromisoformat(chunk["time"]) if chunk["time"] else None

        if not current_conv:
            current_conv.append(chunk)
            continue

        prev_time = datetime.fromisoformat(current_conv[-1]["time"]) if current_conv[-1]["time"] else None

        if chunk_time and prev_time:
            gap = (chunk_time - prev_time).total_seconds()
            if gap > GAP_THRESHOLD:
                conversations.append(current_conv)
                current_conv = [chunk]
                continue

        current_conv.append(chunk)

    if current_conv:
        conversations.append(current_conv)

    # Build conversation metadata
    conv_data = []
    for i, conv in enumerate(conversations):
        first_time = conv[0]["time"]
        last_time = conv[-1]["time"]
        total_duration = sum(c["duration"] for c in conv)
        preview = " | ".join(c["text_preview"][:80] for c in conv[:3])

        conv_info = {
            "id": i + 1,
            "start_time": first_time,
            "end_time": last_time,
            "num_chunks": len(conv),
            "total_duration_sec": round(total_duration, 1),
            "total_duration_min": round(total_duration / 60, 1),
            "chunks": [c["filename"] for c in conv],
            "preview": preview,
        }
        conv_data.append(conv_info)
        print(f"  Conv {i+1}: {first_time} — {len(conv)} chunks, {round(total_duration/60,1)} min")

    output = date_folder / "phase2_segments.json"
    with open(output, "w") as f:
        json.dump(conv_data, f, indent=2)

    print(f"\nPhase 2 done: {len(conv_data)} conversations")
    print(f"Saved: {output}")
    return conv_data


# ═══════════════════════════════════════════
# Phase 3: Concatenate Conversation Audio
# ═══════════════════════════════════════════

def phase3_concatenate(date_folder):
    """Concatenate related chunks into conversation audio files."""
    phase2_file = date_folder / "phase2_segments.json"
    if not phase2_file.exists():
        print("❌ Phase 2 results not found. Run phase 2 first.")
        return []

    with open(phase2_file) as f:
        conversations = json.load(f)

    print(f"Phase 3: Concatenating {len(conversations)} conversations...")

    concat_dir = date_folder / "conversations"
    concat_dir.mkdir(exist_ok=True)

    outputs = []
    for conv in conversations:
        conv_id = conv["id"]
        start = conv["start_time"].replace(":", "-") if conv["start_time"] else f"conv{conv_id}"
        output_name = f"conversation_{conv_id}_{start}.m4a"
        output_path = concat_dir / output_name

        if len(conv["chunks"]) == 1:
            src = date_folder / conv["chunks"][0]
            subprocess.run(["cp", str(src), str(output_path)], check=True)
        else:
            list_file = date_folder / f"_concat_{conv_id}.txt"
            with open(list_file, "w") as f:
                for chunk_name in conv["chunks"]:
                    chunk_path = date_folder / chunk_name
                    f.write(f"file '{chunk_path}'\n")

            result = subprocess.run(
                ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(list_file),
                 "-c", "copy", str(output_path)],
                capture_output=True, text=True
            )
            list_file.unlink(missing_ok=True)

            if result.returncode != 0:
                print(f"  ❌ Conv {conv_id}: ffmpeg error")
                continue

        duration = get_duration(output_path)
        size_mb = output_path.stat().st_size / 1024 / 1024
        print(f"  ✅ Conv {conv_id}: {output_name} ({round(duration/60,1)} min, {round(size_mb,1)} MB)")

        conv["output_file"] = str(output_path)
        conv["output_name"] = output_name
        outputs.append(conv)

    with open(phase2_file, "w") as f:
        json.dump(conversations, f, indent=2)

    print(f"\nPhase 3 done: {len(outputs)} conversation files in {concat_dir}")
    return outputs


# ═══════════════════════════════════════════
# Phase 4: AssemblyAI Diarized Transcription
# ═══════════════════════════════════════════

def phase4_diarize(date_folder):
    """Full AssemblyAI Universal-3 transcription with speaker diarization."""
    aai_key = get_api_key("AssemblyAI", "ASSEMBLYAI_API_KEY", "assemblyai_api_key")

    phase2_file = date_folder / "phase2_segments.json"
    if not phase2_file.exists():
        print("❌ Phase 2 results not found.")
        return

    with open(phase2_file) as f:
        conversations = json.load(f)

    concat_dir = date_folder / "conversations"
    transcript_dir = RECORDINGS_DIR / "transcripts"
    transcript_dir.mkdir(exist_ok=True)

    date_str = date_folder.name
    final_transcript = f"# Watch Recordings — {date_str}\n\n"

    print(f"Phase 4: AssemblyAI diarization on {len(conversations)} conversations...")

    headers = {"authorization": aai_key}

    for conv in conversations:
        conv_id = conv["id"]
        output_file = conv.get("output_file")
        if not output_file or not Path(output_file).exists():
            conv_files = list(concat_dir.glob(f"conversation_{conv_id}_*"))
            if conv_files:
                output_file = str(conv_files[0])
            else:
                print(f"  ⬜ Conv {conv_id}: no audio file, skipping")
                continue

        file_path = Path(output_file)
        size_mb = file_path.stat().st_size / 1024 / 1024
        duration_min = conv.get("total_duration_min", "?")

        print(f"  🔄 Conv {conv_id}: {round(size_mb,1)} MB, ~{duration_min} min — uploading...", flush=True)

        # Upload audio
        upload_resp = requests.post(
            "https://api.assemblyai.com/v2/upload",
            headers=headers,
            data=file_path.read_bytes(),
            timeout=300
        )
        if upload_resp.status_code != 200:
            print(f"  ❌ Upload failed: {upload_resp.status_code}")
            continue
        upload_url = upload_resp.json()["upload_url"]

        # Submit transcription
        transcript_resp = requests.post(
            "https://api.assemblyai.com/v2/transcript",
            headers={**headers, "content-type": "application/json"},
            json={
                "audio_url": upload_url,
                "speech_model": "universal",
                "speaker_labels": True,
                "language_code": "en",
            },
            timeout=30
        )
        if transcript_resp.status_code != 200:
            print(f"  ❌ Submit failed: {transcript_resp.status_code}")
            continue

        transcript_id = transcript_resp.json()["id"]
        print(f"    Submitted: {transcript_id} — polling...", end="", flush=True)

        # Poll for completion
        poll_url = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
        status = None
        while True:
            poll_resp = requests.get(poll_url, headers=headers, timeout=30)
            status = poll_resp.json().get("status")
            if status == "completed":
                print(" ✅")
                break
            elif status == "error":
                print(f" ❌ {poll_resp.json().get('error', 'unknown')}")
                break
            else:
                print(".", end="", flush=True)
                time.sleep(10)

        if status != "completed":
            continue

        result = poll_resp.json()

        # Format diarized transcript
        utterances = result.get("utterances", [])
        if utterances:
            lines = []
            for u in utterances:
                ts_sec = u["start"] / 1000
                mins = int(ts_sec // 60)
                secs = int(ts_sec % 60)
                speaker = u.get("speaker", "?")
                text = u.get("text", "")
                lines.append(f"[{mins:02d}:{secs:02d}] Speaker {speaker}: {text}")
            full_text = "\n".join(lines)
        else:
            full_text = result.get("text") or "[no text]"

        start_time = conv.get("start_time", "unknown")[:16].replace("T", " ")

        final_transcript += f"## Conversation {conv_id} — {start_time} ({duration_min} min)\n\n"
        final_transcript += full_text + "\n\n---\n\n"

        # Save incrementally
        output_path = transcript_dir / f"{date_str}-diarized.md"
        with open(output_path, "w") as f:
            f.write(final_transcript)

        print(f"  ✅ Conv {conv_id}: {len(full_text)} chars, {len(utterances)} utterances")

    output_path = transcript_dir / f"{date_str}-diarized.md"
    with open(output_path, "w") as f:
        f.write(final_transcript)

    print(f"\nPhase 4 done: {output_path}")
    return output_path


# ═══════════════════════════════════════════
# Main
# ═══════════════════════════════════════════

def main():
    if len(sys.argv) < 2:
        print("Wear Audio Transcription Pipeline")
        print()
        print("Usage: transcribe-pipeline.py <date> [--phase 1|2|3|4|all]")
        print()
        print("Phases:")
        print("  1 — Whisper local pass (detect content vs silence)")
        print("  2 — Segment into conversations (by time gaps)")
        print("  3 — Concatenate conversation audio (ffmpeg)")
        print("  4 — Diarized transcription (AssemblyAI)")
        print("  all — Run all phases (default)")
        print()
        print("Example:")
        print("  python3 transcribe-pipeline.py 2025-01-15")
        print("  python3 transcribe-pipeline.py 2025-01-15 --phase 1")
        sys.exit(1)

    date = sys.argv[1]
    date_folder = RECORDINGS_DIR / date

    if not date_folder.exists():
        print(f"❌ Folder not found: {date_folder}")
        sys.exit(1)

    phase = "all"
    if "--phase" in sys.argv:
        idx = sys.argv.index("--phase")
        if idx + 1 < len(sys.argv):
            phase = sys.argv[idx + 1]

    phases = {
        "1": [phase1_whisper_pass],
        "2": [phase2_segment],
        "3": [phase3_concatenate],
        "4": [phase4_diarize],
        "all": [phase1_whisper_pass, phase2_segment, phase3_concatenate, phase4_diarize],
    }

    funcs = phases.get(phase, phases["all"])
    for func in funcs:
        func(date_folder)
        print()


if __name__ == "__main__":
    main()
