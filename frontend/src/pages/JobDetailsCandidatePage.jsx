import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { getJob, listResumes, viewResume } from '../services/resumeService'
import { applyToJob, listMyApplications } from '../services/applicationService'
import SkillList from '../components/SkillList'
import ScoreBadge from '../components/ScoreBadge'

export default function JobDetailsCandidatePage() {
  const { jobId } = useParams()
  const [job, setJob] = useState(null)
  const [resumes, setResumes] = useState([])
  const [application, setApplication] = useState(null)
  const [resumeId, setResumeId] = useState('')
  const [coverNote, setCoverNote] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    Promise.all([getJob(jobId), listResumes(), listMyApplications()])
      .then(([j, rs, apps]) => {
        setJob(j)
        setResumes(rs)
        setApplication(apps.find((a) => a.job_id === jobId) || null)
        if (rs.length) setResumeId(rs[0].id)
      })
      .catch((err) => setError(err.response?.data?.detail || 'Could not load this job.'))
  }, [jobId])

  async function submit(e) {
    e.preventDefault()
    if (!resumeId) return setError('Upload a resume before applying.')
    setLoading(true)
    setError('')
    try {
      const result = await applyToJob(jobId, { resume_id: resumeId, cover_note: coverNote || null })
      setApplication(result)
    } catch (err) {
      setError(err.response?.data?.detail || 'Application failed.')
    } finally {
      setLoading(false)
    }
  }

  if (!job) return <p className="text-slate-500">{error || 'Loading...'}</p>

  const req = job.parsed_requirements || {}

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <Link to="/candidate/jobs" className="text-sm text-indigo-600 hover:underline">← Back to jobs</Link>
          <div className="mt-2 flex items-center gap-3"><h1 className="text-2xl font-semibold text-slate-900">{job.title}</h1><span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-600">{job.status || "active"}</span></div>
        </div>
        {application && <ScoreBadge score={application.match_score ?? 0} />}
      </div>

      <div className="grid gap-4 rounded-2xl border border-white bg-white/85 p-5 shadow-sm backdrop-blur sm:grid-cols-2">
        <SkillList title="Required skills" skills={req.required_skills} variant="matched" />
        <SkillList title="Preferred skills" skills={req.preferred_skills} variant="neutral" />
        <div className="sm:col-span-2">
          <p className="mb-2 text-sm font-semibold text-slate-700">Job description</p>
          <p className="whitespace-pre-wrap text-sm leading-6 text-slate-600">{job.description}</p>
        </div>
      </div>

      {job.status !== "active" && !application ? (
        <div className="rounded-2xl border border-slate-200 bg-slate-50 p-6"><p className="font-semibold text-slate-800">Applications are closed</p><p className="mt-1 text-sm text-slate-500">This job is currently {job.status}. You can still review the job details.</p></div>
      ) : application ? (
        <div className="rounded-2xl border border-white bg-white/85 p-6 shadow-sm backdrop-blur">
          <p className="text-sm font-semibold text-slate-900">Application submitted</p>
          <p className="mt-1 text-sm text-slate-500">Status: <span className="font-medium text-indigo-600">{application.status}</span></p>
          <p className="mt-2 text-sm text-slate-500">AI match score: {Math.round(application.match_score ?? 0)}%</p>
          <Link to="/candidate/applications" className="mt-4 inline-block text-sm font-medium text-indigo-600 hover:underline">View all applications →</Link>
        </div>
      ) : (
        <form onSubmit={submit} className="rounded-2xl border border-white bg-white/85 p-6 shadow-sm backdrop-blur">
          <h2 className="text-lg font-semibold text-slate-900">Apply for this role</h2>
          <p className="mt-1 text-sm text-slate-500">Your selected resume will be parsed and matched against this job.</p>

          {resumes.length ? (
            <>
              <label className="mt-5 block text-sm font-medium text-slate-700">Resume</label>
              <div className="mt-2 flex flex-col gap-2 sm:flex-row">
                <select value={resumeId} onChange={(e) => setResumeId(e.target.value)} className="w-full rounded-md border border-slate-300 px-3 py-2">
                  {resumes.map((r) => <option key={r.id} value={r.id}>{r.file_name}</option>)}
                </select>
                {resumeId && (
                  <button type="button" onClick={() => viewResume(resumeId)} className="shrink-0 rounded-md border border-indigo-200 bg-indigo-50 px-4 py-2 text-sm font-medium text-indigo-700 hover:bg-indigo-100">
                    View Resume ↗
                  </button>
                )}
              </div>

              <label className="mt-4 block text-sm font-medium text-slate-700">Cover note <span className="font-normal text-slate-400">(optional)</span></label>
              <textarea rows={5} maxLength={3000} value={coverNote} onChange={(e) => setCoverNote(e.target.value)} placeholder="A short note to the recruiter..." className="mt-2 w-full rounded-md border border-slate-300 px-3 py-2" />

              {error && <p className="mt-3 text-sm text-rose-600">{error}</p>}
              <button disabled={loading} className="mt-4 rounded-md bg-linear-to-r from-indigo-600 to-violet-600 px-5 py-2.5 text-white shadow-md shadow-indigo-500/25 disabled:opacity-50">
                {loading ? 'Submitting & calculating match...' : 'Apply now'}
              </button>
            </>
          ) : (
            <div className="mt-5 rounded-xl border border-indigo-100 bg-indigo-50/60 p-4">
              <p className="text-sm text-slate-700">You need a parsed resume before applying.</p>
              <Link to="/candidate/upload" className="mt-3 inline-block rounded-md bg-linear-to-r from-indigo-600 to-violet-600 px-4 py-2 text-sm text-white">Upload resume</Link>
            </div>
          )}
        </form>
      )}
    </div>
  )
}
