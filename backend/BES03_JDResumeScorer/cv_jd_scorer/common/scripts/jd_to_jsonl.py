"""
Extract job descriptions from a CSV and parse them into a JSONL corpus.

The CSV is expected to have columns: id, Job, Description.
Each unique Description is parsed via BES03_jd_parser and written as one
JSONL record. Near-empty descriptions are dropped; identical descriptions
are deduped (first id wins).

Usage:
    python jd_to_jsonl.py ../data/jd/selected_job_descriptions.csv
    python jd_to_jsonl.py jds.csv --output /tmp/out.jsonl --min-chars 200
"""
import argparse
import csv
import json
import sys
from pathlib import Path

# sys.path bootstrap — backend/ must be on the path for BES03_jd_parser to be importable
# when this script is run directly (not installed as a package).
# parents[4]: scripts/ → common/ → cv_jd_scorer/ → BES02_JDResumeScorer/ → backend/
_BACKEND = Path(__file__).resolve().parents[4]
if str(_BACKEND) not in sys.path:
    sys.path.insert(0, str(_BACKEND))

from BES02_jd_parser import JD_PARSER_VERSION  # noqa: E402
from BES02_jd_parser.parser import parse_jd  # noqa: E402

_EVAL_RAW_JD = _BACKEND / "BES02_JDResumeScorer" / "eval_data" / "raw_jd"

# CSV description fields can be large; lift the field-size ceiling.
csv.field_size_limit(10**7)


# -- Calls : nothing (leaf)
# -- Called by : _parse_one, _failed_record
def _split_job(job: str) -> tuple[str | None, str | None]:
    """Split a 'Title - Company | Site' label into (title, company)."""
    label = (job or "").split(" | ")[0].strip()
    if " - " in label:
        title, company = label.rsplit(" - ", 1)
        return title.strip() or None, company.strip() or None
    return (label or None), None


# -- Calls : parse_jd, _split_job
# -- Called by : main
def _parse_one(jd_id: str, job: str, description: str) -> dict:
    title, company = _split_job(job)
    parsed = parse_jd(description)
    return {
        "jd_id": jd_id,
        "source_job": job,
        "source_title": title,
        "source_company": company,
        **parsed.model_dump(mode="json"),
    }


# -- Calls : _split_job
# -- Called by : main
def _failed_record(jd_id: str, job: str, exc: Exception) -> dict:
    title, company = _split_job(job)
    return {
        "jd_id": jd_id,
        "source_job": job,
        "source_title": title,
        "source_company": company,
        "parser_version": JD_PARSER_VERSION,
        "raw_text": f"ERROR: {exc}",
        "parse_warnings": ["parse_failed"],
    }


# -- Calls : _parse_one, _failed_record
# -- Called by : __main__
def main(csv_path: Path, output: Path, min_chars: int) -> None:
    total = junk = dup = written = failed = 0
    seen: set[str] = set()

    with csv_path.open(encoding="utf-8", newline="") as src, \
            output.open("w", encoding="utf-8") as out:
        reader = csv.DictReader(src)
        for row in reader:
            total += 1
            jd_id = (row.get("id") or "").strip()
            job = (row.get("Job") or "").strip()
            description = (row.get("Description") or "").strip()

            if len(description) < min_chars:
                junk += 1
                continue
            if description in seen:
                dup += 1
                continue
            seen.add(description)

            try:
                record = _parse_one(jd_id, job, description)
            except Exception as exc:
                record = _failed_record(jd_id, job, exc)
                failed += 1
                print(f"  FAIL id={jd_id}: {exc}", file=sys.stderr)
            out.write(json.dumps(record) + "\n")
            written += 1

    print(f"total={total} junk={junk} dup={dup} written={written} (failed={failed})")
    print(f"Wrote {written} records -> {output}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Extract & parse JDs from a CSV into JSONL.")
    ap.add_argument("csv_path", type=Path, help="CSV with columns: id, Job, Description")
    ap.add_argument(
        "--output", "-o",
        type=Path,
        default=None,
        help="Output JSONL path (default: eval_data/raw_jd/<csv-stem>.jsonl)",
    )
    ap.add_argument(
        "--min-chars",
        type=int,
        default=100,
        help="Drop descriptions shorter than this many characters (default: 100)",
    )
    args = ap.parse_args()

    csv_path: Path = args.csv_path.resolve()
    if not csv_path.is_file():
        ap.error(f"Not a file: {csv_path}")

    output: Path = args.output.resolve() if args.output else _EVAL_RAW_JD / f"{csv_path.stem}.jsonl"
    output.parent.mkdir(parents=True, exist_ok=True)
    main(csv_path, output, args.min_chars)
