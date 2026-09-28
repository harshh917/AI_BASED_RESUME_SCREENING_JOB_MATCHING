"""Pure metric functions (no external deps) for evaluating ranked candidate lists."""
import math
from typing import Dict, List


def precision_recall_f1(ranked_ids: List[str], relevant: set, k: int) -> Dict[str, float]:
    top_k = ranked_ids[:k]
    hits = len([r for r in top_k if r in relevant])
    precision = hits / k if k else 0.0
    recall = hits / len(relevant) if relevant else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
    return {"precision": precision, "recall": recall, "f1": f1}


def ndcg_at_k(ranked_ids: List[str], gains: Dict[str, float], k: int) -> float:
    dcg = sum(gains.get(rid, 0.0) / math.log2(i + 2) for i, rid in enumerate(ranked_ids[:k]))
    ideal = sorted(gains.values(), reverse=True)[:k]
    idcg = sum(g / math.log2(i + 2) for i, g in enumerate(ideal))
    return dcg / idcg if idcg else 0.0


def reciprocal_rank(ranked_ids: List[str], relevant: set) -> float:
    for i, rid in enumerate(ranked_ids, start=1):
        if rid in relevant:
            return 1.0 / i
    return 0.0
