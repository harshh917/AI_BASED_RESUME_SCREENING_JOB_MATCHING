import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { listResumes, listJobs, getRecommendedJobs } from '../services/resumeService'
import StatCard from '../components/StatCard'

export default function CandidateDashboard() {
  const [resumes, setResumes] = useState([])
  const [jobs, setJobs] = useState([])
  const [recommendations, setRecommendations] = useState([])
  useEffect(() => {
    listResumes().then(setResumes).catch(() => {})
    listJobs().then(setJobs).catch(() => {})
    getRecommendedJobs().then(setRecommendations).catch(() => {})
  }, [])
  return (
    <div className="flex flex-col gap-6">
      <h1 className="text-2xl font-semibold text-slate-900">Candidate Dashboard</h1>
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <StatCard label="Resumes uploaded" value={resumes.length} />
        <StatCard label="Open jobs" value={jobs.length} />
      </div>
      {recommendations.length > 0 && <section className="rounded-2xl border border-white bg-white/85 p-5 shadow-sm backdrop-blur">
        <div className="flex items-center justify-between"><div><h2 className="text-lg font-semibold text-slate-900">Recommended for you</h2><p className="text-sm text-slate-500">Based on your parsed resume and the job requirements.</p></div><Link to="/candidate/jobs" className="text-sm text-indigo-600 hover:underline">Browse all →</Link></div>
        <div className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {recommendations.slice(0, 6).map((r) => <Link key={r.job_id} to={`/candidate/jobs/${r.job_id}`} className="rounded-xl border border-slate-100 p-4 hover:border-indigo-200 hover:bg-indigo-50/40">
            <div className="flex items-start justify-between gap-3"><h3 className="font-medium text-slate-900">{r.title}</h3><span className="font-semibold text-indigo-700">{Math.round(r.overall_score)}%</span></div>
            <p className="mt-2 text-xs text-slate-500">Skills {Math.round(r.skill_score)}% · Semantic {Math.round(r.semantic_score)}%</p>
            {r.missing_skills?.length > 0 && <p className="mt-2 text-xs text-amber-700">Missing: {r.missing_skills.slice(0,3).join(', ')}</p>}
          </Link>)}
        </div>
      </section>}
      <div className="flex gap-3">
        <Link to="/candidate/upload" className="rounded-md bg-linear-to-r from-indigo-600 to-violet-600 shadow-md shadow-indigo-500/25 px-4 py-2 text-white hover:brightness-110 hover:-translate-y-0.5">Upload resume</Link>
        <Link to="/candidate/resume" className="rounded-md border border-slate-300 px-4 py-2 hover:bg-slate-100">My resume</Link>
        <Link to="/candidate/jobs" className="rounded-md border border-slate-300 px-4 py-2 hover:bg-slate-100">Browse jobs</Link>
        <Link to="/candidate/applications" className="rounded-md border border-slate-300 px-4 py-2 hover:bg-slate-100">My applications</Link>
      </div>
    </div>
  )
}
