import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { listMyApplications } from '../services/applicationService'

const statusClass = {
  applied: 'bg-indigo-50 text-indigo-700',
  shortlisted: 'bg-emerald-50 text-emerald-700',
  rejected: 'bg-rose-50 text-rose-700',
  hired: 'bg-violet-50 text-violet-700',
}

export default function MyApplicationsPage() {
  const [apps, setApps] = useState([])
  useEffect(() => { listMyApplications().then(setApps).catch(() => {}) }, [])

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-semibold text-slate-900">My Applications</h1>
        <p className="mt-1 text-sm text-slate-500">Track the jobs you have applied to.</p>
      </div>
      <div className="overflow-x-auto rounded-2xl border border-white bg-white/85 shadow-sm backdrop-blur">
        <table className="w-full text-left text-sm">
          <thead className="bg-slate-50 text-slate-600">
            <tr><th className="p-4">Job</th><th className="p-4">Resume</th><th className="p-4">AI match</th><th className="p-4">Status</th><th className="p-4">Applied</th></tr>
          </thead>
          <tbody>
            {apps.map((a) => (
              <tr key={a.id} className="border-t border-slate-100">
                <td className="p-4"><Link to={`/candidate/jobs/${a.job_id}`} className="font-medium text-indigo-600 hover:underline">{a.job_title}</Link></td>
                <td className="p-4 text-slate-600">{a.resume_file_name}</td>
                <td className="p-4 font-semibold text-slate-800">{Math.round(a.match_score ?? 0)}%</td>
                <td className="p-4"><span className={`rounded-full px-3 py-1 text-xs font-semibold ${statusClass[a.status] || 'bg-slate-100 text-slate-600'}`}>{a.status}</span></td>
                <td className="p-4 text-slate-500">{new Date(a.applied_at).toLocaleDateString()}</td>
              </tr>
            ))}
            {!apps.length && <tr><td className="p-6 text-slate-500" colSpan={5}>No applications yet. <Link className="text-indigo-600 hover:underline" to="/candidate/jobs">Browse jobs</Link></td></tr>}
          </tbody>
        </table>
      </div>
    </div>
  )
}
