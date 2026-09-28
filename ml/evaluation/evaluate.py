"""
Evaluate the matching engine against a labels file.

Usage (from repo root):
    python ml/evaluation/evaluate.py --labels ml/evaluation/labels.example.json --k 3

Reports Precision@k / Recall@k / F1@k (relevant = gain >= 1), NDCG@k and MRR
per job, plus the macro average. Metrics are only meaningful if the labels
come from real human judgement. The example labels are NOT ground truth.
"""
import argparse
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "backend"))
sys.path.insert(0, os.path.dirname(__file__))

from app.services.embedding_service import generate_embedding  # noqa: E402
from app.services.jd_parser import parse_job_description  # noqa: E402
from app.services.matching_engine import run_matching  # noqa: E402
from app.services.resume_parser import parse_resume  # noqa: E402
from metrics import ndcg_at_k, precision_recall_f1, reciprocal_rank  # noqa: E402

DATASETS = os.path.join(ROOT, "ml", "datasets")


def rank_resumes(jd_file, resume_files):
    with open(os.path.join(DATASETS, "job_descriptions", jd_file)) as f:
        jd = json.load(f)["description"]
    reqs, job_emb = parse_job_description(jd), generate_embedding(jd)
    scored = []
    for name in resume_files:
        with open(os.path.join(DATASETS, "resumes", name), "rb") as f:
            parsed = parse_resume(name, f.read())
        text = " ".join([parsed.get("summary") or ""] + [p.get("description") or "" for p in parsed["projects"]])
        emb = generate_embedding(text or parsed["raw_text"][:2000])
        scored.append((name, run_matching(reqs, parsed, emb, job_emb)["overall_score"]))
    return [n for n, _ in sorted(scored, key=lambda x: -x[1])]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--labels", required=True)
    ap.add_argument("--k", type=int, default=3)
    args = ap.parse_args()
    with open(args.labels) as f:
        labels = {k: v for k, v in json.load(f).items() if not k.startswith("_")}

    rows = []
    for jd_file, gains in labels.items():
        ranked = rank_resumes(jd_file, list(gains))
        relevant = {r for r, g in gains.items() if g >= 1}
        prf = precision_recall_f1(ranked, relevant, args.k)
        rows.append({**prf, "ndcg": ndcg_at_k(ranked, gains, args.k), "mrr": reciprocal_rank(ranked, relevant)})
        print(f"{jd_file}: ranking={ranked}")
        print("  " + ", ".join(f"{k}@{args.k}={v:.3f}" if k != "mrr" else f"mrr={v:.3f}" for k, v in rows[-1].items()))
    if rows:
        print("MACRO AVG: " + ", ".join(f"{k}={sum(r[k] for r in rows)/len(rows):.3f}" for k in rows[0]))


if __name__ == "__main__":
    main()
