import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { listJobs, getRankedResults, deleteJob } from '../services/resumeService'
import api from '../services/api'
import StatCard from '../components/StatCard'

export default function RecruiterDashboard() {
  const [jobs, setJobs] = useState([])
  const [candidateCount, setCandidateCount] = useState(0)
  const [screened, setScreened] = useState(0)
  const [avg, setAvg] = useState(null)
  const [deletingId, setDeletingId] = useState(null)
  const [error, setError] = useState('')

  async function loadJobs() {
    const j = await listJobs()
    setJobs(j)
    const c = await api.get('/api/candidates')
    setCandidateCount(c.data.length)
    let all = []
    for (const job of j) all = all.concat(await getRankedResults(job.id))
    setScreened(all.length)
    setAvg(all.length ? all.reduce((s, r) => s + r.overall_score, 0) / all.length : null)
  }

  useEffect(() => {
    async function load() {
      await loadJobs()
    }
    load().catch(() => {})
  }, [])

  async function handleDelete(job) {
    const confirmed = window.confirm(`Delete “${job.title}”? This will also remove its applications and matching results.`)
    if (!confirmed) return

    setDeletingId(job.id)
    setError('')
    try {
      await deleteJob(job.id)
      await loadJobs()
    } catch (err) {
      setError(err.response?.data?.detail || 'Unable to delete job')
    } finally {
      setDeletingId(null)
    }
  }

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold text-slate-900">Recruiter Dashboard</h1>
        <Link to="/recruiter/data" className="rounded-md border border-slate-300 px-4 py-2 hover:bg-slate-100">Data</Link>
        <Link to="/recruiter/evaluation" className="rounded-md border border-slate-300 px-4 py-2 hover:bg-slate-100">Evaluation</Link>
        <Link to="/recruiter/jobs/new" className="rounded-md bg-linear-to-r from-indigo-600 to-violet-600 shadow-md shadow-indigo-500/25 px-4 py-2 text-white hover:brightness-110 hover:-translate-y-0.5">Create job</Link>
      </div>
      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        <StatCard label="Total jobs" value={jobs.length} />
        <StatCard label="Total candidates" value={candidateCount} />
        <StatCard label="Resumes screened" value={screened} />
        <StatCard label="Average match score" value={avg === null ? '—' : `${avg.toFixed(0)}%`} />
      </div>
      <div className="rounded-2xl border border-white bg-white/85 shadow-sm backdrop-blur">
        {jobs.length === 0 && <p className="p-4 text-slate-600">No jobs yet.</p>}
        {error && <p className="border-b border-rose-100 bg-rose-50 p-4 text-sm text-rose-600">{error}</p>}
        {jobs.map((j) => (
          <div key={j.id} className="flex items-center justify-between gap-4 border-b border-slate-100 p-4 last:border-0 hover:bg-slate-50">
            <div className="min-w-0 flex-1">
              <Link to={`/recruiter/jobs/${j.id}`} className="truncate text-slate-900 hover:text-indigo-600">{j.title}</Link>
              <span className={`ml-2 rounded-full px-2 py-0.5 text-xs ${j.status === 'active' ? 'bg-emerald-50 text-emerald-700' : 'bg-slate-100 text-slate-600'}`}>{j.status || 'active'}</span>
            </div>
            <Link to={`/recruiter/jobs/${j.id}/edit`} className="shrink-0 rounded-md border border-slate-300 px-3 py-1.5 text-sm hover:bg-slate-100">Edit</Link>
            <button type="button" onClick={() => handleDelete(j)} disabled={deletingId === j.id}
              className="shrink-0 rounded-md border border-rose-200 px-3 py-1.5 text-sm font-medium text-rose-600 hover:bg-rose-50 disabled:cursor-not-allowed disabled:opacity-50">
              {deletingId === j.id ? 'Deleting...' : 'Delete'}
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}
