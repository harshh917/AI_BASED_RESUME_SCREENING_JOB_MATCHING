import { useEffect, useState } from 'react'

// Animated circular score ring. Colour reflects the score band; the label is always shown as text too.
export default function ScoreBadge({ label, score, size = 72 }) {
  const [shown, setShown] = useState(0)
  useEffect(() => { const t = setTimeout(() => setShown(score), 120); return () => clearTimeout(t) }, [score])
  const r = (size - 10) / 2
  const c = 2 * Math.PI * r
  const [from, to] = score >= 75 ? ['#10b981', '#06b6d4'] : score >= 50 ? ['#f59e0b', '#f97316'] : ['#f43f5e', '#ec4899']
  const id = `g${size}${Math.round(score)}${label}`.replace(/\W/g, '')
  return (
    <div className="flex flex-col items-center gap-1">
      <div className="relative" style={{ width: size, height: size }}>
        <svg width={size} height={size} className="-rotate-90">
          <defs><linearGradient id={id}><stop offset="0%" stopColor={from} /><stop offset="100%" stopColor={to} /></linearGradient></defs>
          <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="rgba(148,163,184,.25)" strokeWidth="6" />
          <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke={`url(#${id})`} strokeWidth="6" strokeLinecap="round"
            strokeDasharray={c} strokeDashoffset={c - (c * Math.min(shown, 100)) / 100}
            style={{ transition: 'stroke-dashoffset 1.2s cubic-bezier(.2,.8,.2,1)' }} />
        </svg>
        <span className="font-display absolute inset-0 flex items-center justify-center font-bold text-slate-800" style={{ fontSize: size / 4.2 }}>
          {Math.round(score)}%
        </span>
      </div>
      {label && <span className="text-xs font-medium text-slate-500">{label}</span>}
    </div>
  )
}
