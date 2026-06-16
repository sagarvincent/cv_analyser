"""
Batch-parse a directory of PDFs and write results to a JSONL file.

Usage:
    python pdf_to_jsonl.py /path/to/cv_dir
    python pdf_to_jsonl.py /path/to/cv_dir --output /tmp/results.jsonl
"""
import argparse
import json
import sys
from pathlib import Path

# sys.path bootstrap — backend/ must be on the path for BES01_cv_parser to be importable
# when this script is run directly (not installed as a package).
# parents[4]: scripts/ → common/ → cv_jd_scorer/ → BES02_JDResumeScorer/ → backend/
_BACKEND = Path(__file__).resolve().parents[4]
if str(_BACKEND) not in sys.path:
    sys.path.insert(0, str(_BACKEND))

from BES01_cv_parser import PARSER_VERSION  # noqa: E402
from BES01_cv_parser.parser import parse_cv  # noqa: E402

_EVAL_RAW = _BACKEND / "BES02_JDResumeScorer" / "eval_data" / "raw"


# -- Calls : nothing (leaf)
# -- Called by : main
def _find_pdfs(directory: Path) -> list[Path]:
    return sorted(directory.glob("*.pdf"))


# -- Calls : parse_cv
# -- Called by : main
def _parse_one(pdf_path: Path) -> dict:
    result = parse_cv(pdf_path.read_bytes(), pdf_path.name)
    return {
        "filename": pdf_path.name,
        "parser_version": PARSER_VERSION,
        "raw_text": result.raw_text,
        "sections": result.sections.model_dump(mode="json"),
        "extraction_method": result.extraction_method,
        "ats_redflags": result.ats_redflags.model_dump(mode="json"),
    }


# -- Calls : nothing (leaf)
# -- Called by : main
def _failed_record(pdf_path: Path, exc: Exception) -> dict:
    return {
        "filename": pdf_path.name,
        "parser_version": PARSER_VERSION,
        "raw_text": f"ERROR: {exc}",
        "sections": {},
        "extraction_method": "failed",
        "ats_redflags": {},
    }


# -- Calls : _find_pdfs, _parse_one, _failed_record
# -- Called by : __main__
def main(directory: Path, output: Path) -> None:
    pdfs = _find_pdfs(directory)
    if not pdfs:
        print(f"No PDFs found in {directory}")
        return

    with output.open("w", encoding="utf-8") as fh:
        for pdf_path in pdfs:
            try:
                record = _parse_one(pdf_path)
                print(f"  ok  {pdf_path.name}")
            except Exception as exc:
                record = _failed_record(pdf_path, exc)
                print(f"  FAIL {pdf_path.name}: {exc}", file=sys.stderr)
            fh.write(json.dumps(record) + "\n")

    print(f"\nWrote {len(pdfs)} records -> {output}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Batch-parse PDFs in a directory to a JSONL file.")
    ap.add_argument("directory", type=Path, help="Directory containing PDF files")
    ap.add_argument(
        "--output", "-o",
        type=Path,
        default=None,
        help="Output JSONL path (default: eval_data/raw/<dir-name>.jsonl)",
    )
    args = ap.parse_args()

    directory: Path = args.directory.resolve()
    if not directory.is_dir():
        ap.error(f"Not a directory: {directory}")

    output: Path = args.output.resolve() if args.output else _EVAL_RAW / f"{directory.name}.jsonl"
    output.parent.mkdir(parents=True, exist_ok=True)
    main(directory, output)
