"""
Turns a matching_engine result into a human-readable explanation.

Template-based, not generative — every sentence is built directly from the
computed scores/lists so nothing is invented. Per the assignment brief:
"If information is absent, say 'Not identified in the submitted resume'
rather than assuming it is missing."
"""
from typing import Any, Dict


def build_explanation(match_result: Dict[str, Any], job_title: str = "this role") -> str:
    overall = match_result["overall_score"]
    matched = match_result.get("matched_skills") or []
    missing = match_result.get("missing_skills") or []
    years = match_result.get("estimated_candidate_years", 0)

    lines = [f"Overall Match: {overall:.0f}%", ""]

    if matched:
        lines.append("Strong Matches:")
        lines.extend(f"- {skill}" for skill in matched)
    else:
        lines.append("Strong Matches: Not identified in the submitted resume")

    lines.append("")
    if missing:
        lines.append("Missing / Unclear:")
        lines.extend(f"- {skill}" for skill in missing)
    else:
        lines.append("Missing / Unclear: None of the required skills were missing")

    lines.append("")
    if years:
        lines.append(f"Relevant Experience: approximately {years} year(s) (estimated from resume)")
    else:
        lines.append("Relevant Experience: Not identified in the submitted resume")

    lines.append("")
    summary = _summary_sentence(overall, matched, missing, job_title)
    lines.append(f"Explanation:\n{summary}")

    return "\n".join(lines)


def _summary_sentence(overall: float, matched, missing, job_title: str) -> str:
    if overall >= 75:
        strength = "strong alignment"
    elif overall >= 50:
        strength = "moderate alignment"
    else:
        strength = "limited alignment"

    sentence = f"The candidate demonstrates {strength} with the requirements for {job_title}."
    if matched:
        sentence += f" Key matched areas include {', '.join(matched[:5])}."
    if missing:
        sentence += f" {', '.join(missing[:5])} were not clearly identified in the resume."
    return sentence
