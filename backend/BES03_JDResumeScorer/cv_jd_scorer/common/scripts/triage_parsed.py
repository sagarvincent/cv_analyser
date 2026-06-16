"""
Triage a parsed-CV JSONL into trust buckets.

Reads the output of pdf_to_jsonl.py and splits rows into:
    parsed_ok.jsonl       — trustworthy for eval-data generation
    parsed_suspect.jsonl  — parsed, but quality signals say inspect first
    parse_failures.jsonl  — hard failures (no usable text)

Each suspect row gains a "triage_reasons" list naming the failed checks.

Usage:
    python triage_parsed.py path/to/ENGINEERING.jsonl
    python triage_parsed.py path/to/ENGINEERING.jsonl --outdir /tmp/triaged
"""
import argparse
import json
import sys
from collections import Counter
from pathlib import Path

# --- thresholds: calibrate by inspecting ~10 rows per bucket on a 100-CV
#     sample before trusting a full run
MIN_SECTION_COHERENCE = 0.15
MIN_HEADING_DETECTION = 0.30
MAX_UNCLASSIFIED_RATIO = 0.40


# -- Calls : nothing (leaf)
# -- Called by : triage_record
def _suspect_reasons(rec: dict) -> list[str]:
    flags = rec.get("ats_redflags", {})
    sections = rec.get("sections", {})
    reasons: list[str] = []

    if flags.get("section_coherence", 0.0) < MIN_SECTION_COHERENCE:
        reasons.append(f"section_coherence<{MIN_SECTION_COHERENCE}")
    if flags.get("heading_detection_rate", 0.0) < MIN_HEADING_DETECTION:
        reasons.append(f"heading_detection_rate<{MIN_HEADING_DETECTION}")
    if flags.get("unclassified_ratio", 0.0) > MAX_UNCLASSIFIED_RATIO:
        reasons.append(f"unclassified_ratio>{MAX_UNCLASSIFIED_RATIO}")
    if flags.get("experience_boundary_failures", 0) > 0:
        reasons.append("experience_boundary_failure")
    if not sections.get("education") and "education" in rec.get("raw_text", "").lower():
        reasons.append("education_missed")
    if not sections.get("experience"):
        reasons.append("no_experience_entries")
    return reasons


# -- Calls : _suspect_reasons
# -- Called by : main
def triage_record(rec: dict) -> tuple[str, dict]:
    if rec.get("extraction_method") == "failed" or not rec.get("raw_text", "").strip():
        return "failures", rec
    reasons = _suspect_reasons(rec)
    if reasons:
        return "suspect", {**rec, "triage_reasons": reasons}
    return "ok", rec


# -- Calls : triage_record
# -- Called by : __main__
def main(in_path: Path, outdir: Path) -> None:
    buckets: dict[str, list[dict]] = {"ok": [], "suspect": [], "failures": []}
    with in_path.open(encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                bucket, rec = triage_record(json.loads(line))
                buckets[bucket].append(rec)

    outdir.mkdir(parents=True, exist_ok=True)
    names = {"ok": "parsed_ok.jsonl", "suspect": "parsed_suspect.jsonl", "failures": "parse_failures.jsonl"}
    for bucket, records in buckets.items():
        with (outdir / names[bucket]).open("w", encoding="utf-8") as fh:
            for rec in records:
                fh.write(json.dumps(rec) + "\n")

    total = sum(len(v) for v in buckets.values())
    print(f"{in_path.name}: {total} records")
    for bucket in ("ok", "suspect", "failures"):
        print(f"  {bucket:8s} {len(buckets[bucket]):5d}  ({len(buckets[bucket]) / total:.1%})")
    if buckets["suspect"]:
        reason_counts = Counter(r for rec in buckets["suspect"] for r in rec["triage_reasons"])
        print("  suspect reasons:")
        for reason, n in reason_counts.most_common():
            print(f"    {n:4d}  {reason}")
    print(f"\nWrote buckets -> {outdir}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Triage parsed-CV JSONL into ok/suspect/failure buckets.")
    ap.add_argument("input", type=Path, help="Parsed JSONL produced by pdf_to_jsonl.py")
    ap.add_argument(
        "--outdir",
        type=Path,
        default=None,
        help="Output directory (default: <input-dir>/triaged/<input-stem>)",
    )
    args = ap.parse_args()

    in_path: Path = args.input.resolve()
    if not in_path.is_file():
        ap.error(f"Not a file: {in_path}")

    outdir: Path = args.outdir.resolve() if args.outdir else in_path.parent / "triaged" / in_path.stem
    main(in_path, outdir)
