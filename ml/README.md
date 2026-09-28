# ML / Evaluation

- `datasets/` — synthetic (fictional) resumes and job descriptions. Regenerate PDFs with `python generate_sample_data.py`.
- `evaluation/` — metric functions (`metrics.py`) and the runner (`evaluate.py`).
- `notebooks/`, `experiments/` — for your own analysis (empty placeholders).

```bash
python ml/evaluation/evaluate.py --labels ml/evaluation/labels.example.json --k 3
```

**Important:** `labels.example.json` is illustrative only and was written by the developer. It exists to prove the evaluation code runs. Do not report its output as accuracy. Have real recruiters label a larger set, then report the metrics from that.
