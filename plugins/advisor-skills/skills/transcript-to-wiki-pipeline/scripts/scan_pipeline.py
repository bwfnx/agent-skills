#!/usr/bin/env python3
"""Scan the SBDC Zoom archive transcript pipeline."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def find_file(folder: Path, suffix: str) -> Path | None:
    if not folder.exists():
        return None
    matches = sorted(folder.glob(f"*{suffix}"))
    return matches[0] if matches else None


def scan(archive: Path) -> list[dict[str, str]]:
    manifest = archive / "00_Master Index" / "zoom-training-media-manifest.csv"
    rows: list[dict[str, str]] = []
    with manifest.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            session_id = row["session_id"]
            transcript_dir = archive / "02_Transcripts" / session_id
            reviewed_dir = archive / "03_Reviewed Summaries"
            claromentis_dir = archive / "04_Claromentis Drafts"
            wiki_dir = archive / "05_Wiki Inputs"

            transcript = find_file(transcript_dir, "-transcript.md")
            reviewed = reviewed_dir / f"{session_id}-reviewed-summary.md"
            claromentis = claromentis_dir / f"{session_id}-claromentis-draft.md"
            wiki = wiki_dir / f"{session_id}-wiki-input.md"

            transcript_status = row.get("transcript_status", "")
            if transcript_status == "missing_source_transcript":
                state = "missing_transcript"
            elif transcript and reviewed.exists() and claromentis.exists() and wiki.exists():
                state = "complete"
            elif transcript:
                state = "needs_processing"
            else:
                state = "no_transcript_file"

            rows.append(
                {
                    "session_id": session_id,
                    "series": row.get("series", ""),
                    "session_date": row.get("session_date", ""),
                    "transcript_status": transcript_status,
                    "review_status": row.get("review_status", ""),
                    "state": state,
                    "transcript": str(transcript) if transcript else "",
                    "reviewed_summary_exists": str(reviewed.exists()).lower(),
                    "claromentis_draft_exists": str(claromentis.exists()).lower(),
                    "wiki_input_exists": str(wiki.exists()).lower(),
                }
            )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Scan SBDC transcript pipeline state.")
    parser.add_argument("--archive", default="sbdc-advising/raw/training-media/zoom-archive")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of table text.")
    args = parser.parse_args()

    rows = scan(Path(args.archive))
    if args.json:
        print(json.dumps(rows, indent=2))
        return

    for row in rows:
        if row["state"] in {"complete", "needs_processing", "missing_transcript", "no_transcript_file"}:
            print(
                f"{row['session_date']} {row['session_id']} | "
                f"{row['state']} | transcript={row['transcript_status']} | review={row['review_status']}"
            )


if __name__ == "__main__":
    main()
