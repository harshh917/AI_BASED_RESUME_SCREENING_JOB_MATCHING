export default function SkillList({ title, skills, variant, emptyText = 'Not identified in the submitted resume' }) {
  const styles = variant === 'matched' ? 'bg-emerald-50 text-emerald-700 border-emerald-200' : 'bg-slate-50 text-slate-600 border-slate-200'
  const mark = variant === 'matched' ? '✓' : '○'
  return (
    <div>
      <h3 className="mb-2 text-sm font-semibold text-slate-800">{title}</h3>
      {skills && skills.length > 0 ? (
        <div className="flex flex-wrap gap-2">
          {skills.map((s) => (
            <span key={s} className={`rounded-full border px-3 py-1 text-sm font-medium card-lift ${styles}`}>{mark} {s}</span>
          ))}
        </div>
      ) : (
        <p className="text-sm text-slate-500">{emptyText}</p>
      )}
    </div>
  )
}
