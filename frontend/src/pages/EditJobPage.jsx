import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { getJob, updateJob } from '../services/resumeService'

export default function EditJobPage() {
  const { jobId } = useParams()
  const navigate = useNavigate()
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [status, setStatus] = useState('active')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    getJob(jobId).then((job) => {
      setTitle(job.title); setDescription(job.description); setStatus(job.status || 'active')
    }).catch((e) => setError(e.response?.data?.detail || 'Could not load job.'))
  }, [jobId])

  async function submit(e) {
    e.preventDefault(); setLoading(true); setError('')
    try {
      await updateJob(jobId, { title, description, status })
      navigate(`/recruiter/jobs/${jobId}`)
    } catch (e) {
      setError(e.response?.data?.detail || 'Could not update job.')
    } finally { setLoading(false) }
  }

  return (
    <form onSubmit={submit} className="mx-auto flex w-full max-w-3xl flex-col gap-5 rounded-2xl border border-white bg-white/85 p-6 shadow-sm backdrop-blur">
      <div>
        <Link to={`/recruiter/jobs/${jobId}`} className="text-sm text-indigo-600 hover:underline">← Back to job</Link>
        <h1 className="mt-2 text-2xl font-semibold text-slate-900">Edit job</h1>
      </div>
      <label className="text-sm font-medium text-slate-700">Job title<input value={title} onChange={e=>setTitle(e.target.value)} required className="mt-2 w-full rounded-md border border-slate-300 px-3 py-2" /></label>
      <label className="text-sm font-medium text-slate-700">Job description<textarea value={description} onChange={e=>setDescription(e.target.value)} required rows={14} className="mt-2 w-full rounded-md border border-slate-300 px-3 py-2" /></label>
      <label className="text-sm font-medium text-slate-700">Job status
        <select value={status} onChange={e=>setStatus(e.target.value)} className="mt-2 w-full rounded-md border border-slate-300 bg-white px-3 py-2">
          <option value="active">Active — candidates can apply</option>
          <option value="closed">Closed — applications disabled</option>
          <option value="draft">Draft — not visible to candidates</option>
        </select>
      </label>
      {error && <p className="text-sm text-rose-600">{error}</p>}
      <button disabled={loading} className="rounded-md bg-linear-to-r from-indigo-600 to-violet-600 px-5 py-2.5 text-white disabled:opacity-50">{loading ? 'Saving...' : 'Save changes'}</button>
    </form>
  )
}
