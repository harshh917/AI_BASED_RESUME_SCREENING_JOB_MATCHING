import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { getJob, runMatchingForJob, getRankedResults, deleteJob, getJobStats } from '../services/resumeService'
import SkillList from '../components/SkillList'
import ScoreBadge from '../components/ScoreBadge'

export default function JobDetailsPage() {
  const { jobId } = useParams()
  const navigate = useNavigate()
  const [job, setJob] = useState(null)
  const [ranked, setRanked] = useState([])
  const [minScore, setMinScore] = useState(0)
  const [running, setRunning] = useState(false)
  const [error, setError] = useState('')
  const [deleting, setDeleting] = useState(false)
  const [stats, setStats] = useState(null)

  async function refresh() {
    setRanked(await getRankedResults(jobId))
  }
  useEffect(() => {
    getJob(jobId).then(setJob).catch(() => setError('Job not found'))
    getJobStats(jobId).then(setStats).catch(() => {})
    refresh().catch(() => {})
  }, [jobId])

  async function run() {
    setRunning(true)
    setError('')
    try { await runMatchingForJob(jobId); await refresh() }
    catch (err) { setError(err.response?.data?.detail || 'Matching failed') }
    finally { setRunning(false) }
  }


  async function handleDelete() {
    const confirmed = window.confirm(`Delete “${job.title}”? This will also remove its applications and matching results.`)
    if (!confirmed) return

    setDeleting(true)
    setError('')
    try {
      await deleteJob(jobId)
      navigate('/recruiter')
    } catch (err) {
      setError(err.response?.data?.detail || 'Unable to delete job')
    } finally {
      setDeleting(false)
    }
  }

  if (!job) return <p className="text-slate-500">{error || 'Loading...'}</p>
  const req = job.parsed_requirements || {}
  const visible = ranked.filter((r) => r.overall_score >= minScore)

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center gap-3"><h1 className="text-2xl font-semibold text-slate-900">{job.title}</h1><span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-600">{job.status || "active"}</span></div>
      <div className="grid gap-4 rounded-2xl border border-white bg-white/85 shadow-sm backdrop-blur p-4 sm:grid-cols-2">
        <SkillList title="Required skills" skills={req.required_skills} variant="matched" />
        <SkillList title="Preferred skills" skills={req.preferred_skills} variant="neutral" />
        <p className="text-sm text-slate-600">Minimum experience: {req.experience?.min_years ?? 'Not identified'} years</p>
      </div>
      <div className="flex items-center gap-4">
        <Link to={`/recruiter/jobs/${jobId}/edit`} className="rounded-md border border-slate-300 px-4 py-2 text-sm hover:bg-slate-100">Edit job</Link>
        <Link to={`/recruiter/jobs/${jobId}/applications`} className="rounded-md border border-slate-300 px-4 py-2 text-sm hover:bg-slate-100">View applications</Link>
        <button onClick={handleDelete} disabled={deleting} className="rounded-md border border-rose-200 px-4 py-2 text-sm font-medium text-rose-600 hover:bg-rose-50 disabled:opacity-50">{deleting ? 'Deleting...' : 'Delete job'}</button>
        <button onClick={run} disabled={running} className="rounded-md bg-linear-to-r from-indigo-600 to-violet-600 shadow-md shadow-indigo-500/25 px-4 py-2 text-white disabled:opacity-50">
          {running ? 'Running...' : 'Run matching on all candidates'}
        </button>
        <label className="text-sm text-slate-600">Min score: {minScore}%
          <input type="range" min="0" max="100" value={minScore} onChange={(e) => setMinScore(+e.target.value)} className="ml-2 align-middle" />
        </label>
      </div>
      {error && <p className="text-sm text-rose-600">{error}</p>}
      {stats && <div className="grid grid-cols-2 gap-3 sm:grid-cols-5">
        {[
          ['Applications', stats.applications], ['Applied', stats.applied], ['Shortlisted', stats.shortlisted],
          ['Rejected', stats.rejected], ['Hired', stats.hired]
        ].map(([label, value]) => <div key={label} className="rounded-xl border border-slate-100 bg-white p-4"><p className="text-xs text-slate-500">{label}</p><p className="mt-1 text-xl font-semibold text-slate-900">{value}</p></div>)}
      </div>}
      <div className="overflow-x-auto rounded-2xl border border-white bg-white/85 shadow-sm backdrop-blur">
        <table className="w-full text-left text-sm">
          <thead className="bg-slate-50 text-slate-600">
            <tr><th className="p-3">Rank</th><th className="p-3">Candidate</th><th className="p-3">Match</th><th className="p-3">Skill</th><th className="p-3">Experience</th><th className="p-3">Missing skills</th><th className="p-3"></th></tr>
          </thead>
          <tbody>
            {visible.map((r) => (
              <tr key={r.match_id} className="border-t border-slate-100">
                <td className="p-3">{r.rank}</td>
                <td className="p-3">{r.candidate_name}</td>
                <td className="p-3"><ScoreBadge label="" score={r.overall_score} /></td>
                <td className="p-3">{Math.round(r.skill_score)}%</td>
                <td className="p-3">{Math.round(r.experience_score)}%</td>
                <td className="p-3">{r.missing_skills.length ? r.missing_skills.join(', ') : '—'}</td>
                <td className="p-3"><Link className="underline" to={`/recruiter/jobs/${jobId}/candidates/${r.resume_id}`}>Details</Link></td>
              </tr>
            ))}
            {visible.length === 0 && <tr><td className="p-4 text-slate-500" colSpan={7}>No results. Run matching to rank candidates.</td></tr>}
          </tbody>
        </table>
      </div>
      <p className="text-xs text-slate-500">Scores are decision support only. Protected attributes are never used.</p>
    </div>
  )
}
