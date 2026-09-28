import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { listJobs } from '../services/resumeService'
import { listMyApplications } from '../services/applicationService'
import SkillList from '../components/SkillList'

export default function JobBrowsePage() {
  const [jobs, setJobs] = useState([])
  const [applications, setApplications] = useState([])
  const [error, setError] = useState('')

  useEffect(() => {
    Promise.all([listJobs(), listMyApplications()])
      .then(([jobData, appData]) => { setJobs(jobData); setApplications(appData) })
      .catch(() => setError('Could not load jobs.'))
  }, [])

  const applied = new Map(applications.map((a) => [a.job_id, a]))

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-semibold text-slate-900">Open Jobs</h1>
        <p className="mt-1 text-sm text-slate-500">Browse roles and apply with your parsed resume.</p>
      </div>

      {error && <p className="text-sm text-rose-600">{error}</p>}
      {jobs.length === 0 && <div className="rounded-2xl border border-white bg-white/85 p-6 text-slate-600 shadow-sm backdrop-blur">No jobs posted yet.</div>}

      <div className="grid gap-4">
        {jobs.map((j) => {
          const app = applied.get(j.id)
          return (
            <div key={j.id} className="card-lift rounded-2xl border border-white bg-white/85 p-5 shadow-sm backdrop-blur">
              <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
                <div>
                  <h2 className="text-lg font-semibold text-slate-900">{j.title}</h2>
                  <div className="mt-3">
                    <SkillList title="Required skills" skills={j.parsed_requirements?.required_skills} variant="neutral" />
                  </div>
                </div>
                <div className="shrink-0">
                  {app ? (
                    <Link to={`/candidate/jobs/${j.id}`} className="rounded-md border border-indigo-200 bg-indigo-50 px-4 py-2 text-sm font-medium text-indigo-700 hover:bg-indigo-100">
                      Applied · {app.status}
                    </Link>
                  ) : (
                    <Link to={`/candidate/jobs/${j.id}`} className="rounded-md bg-linear-to-r from-indigo-600 to-violet-600 px-4 py-2 text-sm font-medium text-white shadow-md shadow-indigo-500/25 hover:brightness-110 hover:-translate-y-0.5">
                      View & apply
                    </Link>
                  )}
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
