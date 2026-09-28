import { CountUp } from '../hooks/useReveal'

export default function StatCard({ label, value, accent = 'from-indigo-500 to-violet-500' }) {
  const numeric = typeof value === 'number'
  return (
    <div className="card-lift relative overflow-hidden rounded-2xl border border-white bg-white/80 p-5 shadow-sm backdrop-blur">
      <div className={`absolute -right-6 -top-6 h-20 w-20 rounded-full bg-gradient-to-br ${accent} opacity-20 blur-xl`} />
      <p className="text-sm font-medium text-slate-500">{label}</p>
      <p className="font-display mt-1 text-3xl font-bold text-slate-900">{numeric ? <CountUp to={value} /> : value}</p>
    </div>
  )
}
