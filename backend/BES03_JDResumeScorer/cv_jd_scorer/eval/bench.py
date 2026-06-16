"""
Cross-engine benchmark harness.

Usage:
    python -m cv_jd_scorer.eval.bench
    python -m cv_jd_scorer.eval.bench --engines v1_tfidf v2_ml
    python -m cv_jd_scorer.eval.bench --data path/to/pairs.jsonl
"""
import argparse
import json
import time
from collections import defaultdict

from cv_jd_scorer.engine_registry import _REGISTRY, _load_engine

_DEFAULT_DATA = "backend/BES02_JDResumeScorer/eval_data/labelled/pairs.jsonl"

_TYPES = ("high_match", "confusing", "high_mismatch")
_SUBSCORES = ("keyword_overlap", "seniority", "domain", "skills", "experience")


def _mae(predicted: list[float], expected: list[float]) -> float:
    if not predicted:
        return float("nan")
    return sum(abs(p - e) for p, e in zip(predicted, expected)) / len(predicted)


def run_bench(engine_ids: list[str], data_path: str) -> None:
    pairs = [json.loads(line) for line in open(data_path, encoding="utf-8") if line.strip()]
    if not pairs:
        print(f"No pairs found in {data_path}")
        return

    for engine_id in engine_ids:
        try:
            engine = _load_engine(engine_id)
        except Exception as exc:
            print(f"\n=== {engine_id} --- SKIPPED: {exc}")
            continue

        all_predicted: list[float] = []
        all_expected: list[float] = []

        by_type: dict[str, dict] = {
            t: {"predicted": [], "expected": []} for t in _TYPES
        }

        sub_predicted: dict[str, list[float]] = defaultdict(list)
        sub_expected: dict[str, list[float]] = defaultdict(list)

        elapsed = 0.0
        skipped = False

        for pair in pairs:
            try:
                t0 = time.perf_counter()
                result = engine.compute(pair["parsed_cv"], pair["jd_text"])
                elapsed += time.perf_counter() - t0
            except NotImplementedError:
                print(f"\n=== {engine_id} --- SKIPPED: engine not yet implemented")
                skipped = True
                break

            predicted_score = result.jdFitSummary.score
            expected_score = pair["expected_jd_score"]
            label = pair["match_label"]

            all_predicted.append(predicted_score)
            all_expected.append(expected_score)

            if label in by_type:
                by_type[label]["predicted"].append(predicted_score)
                by_type[label]["expected"].append(expected_score)

            # Sub-score comparison -- only populated if engine exposes a sub_scores dict
            engine_subs: dict = getattr(result, "sub_scores", None) or {}
            expected_subs: dict = pair.get("expected_subscores", {})
            for dim in _SUBSCORES:
                if dim in engine_subs and dim in expected_subs:
                    sub_predicted[dim].append(engine_subs[dim])
                    sub_expected[dim].append(expected_subs[dim])

        if skipped:
            continue

        n = len(pairs)
        total_mae = _mae(all_predicted, all_expected)
        avg_latency_ms = (elapsed / n * 1000) if n else 0.0

        print(f"\n=== {engine_id} ===")
        print(f"  n_pairs          : {n}")
        print(f"  total MAE        : {total_mae:.2f}")

        for t in _TYPES:
            bucket = by_type[t]
            n_t = len(bucket["predicted"])
            mae_t = _mae(bucket["predicted"], bucket["expected"])
            print(f"  -- {t:<16} MAE: {mae_t:.2f}  (n={n_t})")

        sub_parts = []
        for dim in _SUBSCORES:
            if sub_predicted[dim]:
                mae_d = _mae(sub_predicted[dim], sub_expected[dim])
                sub_parts.append(f"{dim}={mae_d:.2f}")
        if sub_parts:
            print(f"  subscore MAE     : {' '.join(sub_parts)}")
        else:
            print(f"  subscore MAE     : n/a (engine does not expose sub_scores)")

        print(f"  avg latency      : {avg_latency_ms:.1f} ms/pair")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Compare scoring engines against labelled pairs.")
    ap.add_argument("--engines", nargs="+", default=list(_REGISTRY), help="Engine IDs to benchmark")
    ap.add_argument("--data", default=_DEFAULT_DATA, help="Path to JSONL file with labelled pairs")
    args = ap.parse_args()
    run_bench(args.engines, args.data)
