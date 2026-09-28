export default function EvaluationPage() {
  return (
    <div className="flex flex-col gap-6">
      <div><h1 className="text-2xl font-semibold text-slate-900">Model Evaluation</h1><p className="mt-1 text-sm text-slate-500">Evaluate ranking quality using human-labelled resume–job pairs.</p></div>
      <div className="grid gap-4 sm:grid-cols-3">
        {['Precision@K','Recall@K','F1@K'].map((m)=><div key={m} className="rounded-2xl border border-white bg-white/85 p-5 shadow-sm"><p className="text-sm text-slate-500">{m}</p><p className="mt-2 text-2xl font-semibold text-slate-400">Not measured</p><p className="mt-1 text-xs text-slate-500">Requires real labelled data.</p></div>)}
      </div>
      <div className="rounded-2xl border border-white bg-white/85 p-6 shadow-sm">
        <h2 className="font-semibold text-slate-900">Evaluation pipeline</h2>
        <ol className="mt-3 list-decimal space-y-2 pl-5 text-sm text-slate-600">
          <li>Collect recruiter/human relevance labels for resume–JD pairs.</li>
          <li>Run the deterministic matching engine and rank candidates.</li>
          <li>Compute Precision@K, Recall@K, F1@K, NDCG@K and MRR.</li>
          <li>Report results only for the labelled population and dataset version used.</li>
        </ol>
        <pre className="mt-5 overflow-x-auto rounded-xl bg-slate-900 p-4 text-xs text-slate-100">python ml/evaluation/evaluate.py --labels ml/evaluation/labels.example.json --k 3</pre>
        <p className="mt-3 text-xs text-slate-500">The bundled labels are illustrative examples, not ground truth. Do not use them to claim production accuracy.</p>
      </div>
    </div>
  )
}
