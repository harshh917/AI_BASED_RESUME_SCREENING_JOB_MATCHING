import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { getJob, viewResume } from '../services/resumeService'
import { listJobApplications, updateApplicationStatus } from '../services/applicationService'

const statuses = ['applied', 'shortlisted', 'rejected', 'hired']

export default function RecruiterApplicationsPage() {
  const { jobId } = useParams()
  const [job, setJob] = useState(null)
  const [apps, setApps] = useState([])
  const [error, setError] = useState('')

  async function load() {
    const [j, a] = await Promise.all([getJob(jobId), listJobApplications(jobId)])
    setJob(j); setApps(a)
  }
  useEffect(() => { load().catch((err) => setError(err.response?.data?.detail || 'Could not load applications.')) }, [jobId])

  async function changeStatus(id, status) {
    try {
      const updated = await updateApplicationStatus(id, status)
      setApps((old) => old.map((a) => a.id === id ? updated : a))
    } catch (err) {
      setError(err.response?.data?.detail || 'Could not update status.')
    }
  }

  if (!job) return <p className="text-slate-500">{error || 'Loading...'}</p>

  return (
    <div className="flex flex-col gap-6">
      <div>
        <Link to={`/recruiter/jobs/${jobId}`} className="text-sm text-indigo-600 hover:underline">← Back to job</Link>
        <h1 className="mt-2 text-2xl font-semibold text-slate-900">Applications · {job.title}</h1>
        <p className="mt-1 text-sm text-slate-500">{apps.length} application{apps.length === 1 ? '' : 's'} · sorted by AI match score</p>
      </div>
      {error && <p className="text-sm text-rose-600">{error}</p>}
      <div className="overflow-x-auto rounded-2xl border border-white bg-white/85 shadow-sm backdrop-blur">
        <table className="w-full text-left text-sm">
          <thead className="bg-slate-50 text-slate-600">
            <tr><th className="p-4">Candidate</th><th className="p-4">AI match</th><th className="p-4">Resume</th><th className="p-4">Status</th><th className="p-4">Applied</th></tr>
          </thead>
          <tbody>
            {apps.map((a) => (
              <tr key={a.id} className="border-t border-slate-100">
                <td className="p-4"><p className="font-medium text-slate-900">{a.candidate_name}</p><p className="text-xs text-slate-500">{a.candidate_email}</p></td>
                <td className="p-4 font-semibold text-indigo-700">{Math.round(a.match_score ?? 0)}%</td>
                <td className="p-4">
                  <button type="button" onClick={() => viewResume(a.resume_id)} className="text-indigo-600 hover:underline">
                    View Resume ↗
                  </button>
                  <p className="mt-1 max-w-48 truncate text-xs text-slate-500">{a.resume_file_name}</p>
                </td>
                <td className="p-4">
                  <select value={a.status} onChange={(e) => changeStatus(a.id, e.target.value)} className="rounded-md border border-slate-300 bg-white px-2 py-1.5 text-xs">
                    {statuses.map((s) => <option key={s} value={s}>{s}</option>)}
                  </select>
                </td>
                <td className="p-4 text-slate-500">{new Date(a.applied_at).toLocaleDateString()}</td>
              </tr>
            ))}
            {!apps.length && <tr><td className="p-6 text-slate-500" colSpan={5}>No applications yet.</td></tr>}
          </tbody>
        </table>
      </div>
    </div>
  )
}
