import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { createJob } from '../services/resumeService'

export default function CreateJobPage() {
  const [form, setForm] = useState({ title: '', description: '' })
  const [error, setError] = useState('')
  const navigate = useNavigate()

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    try {
      const job = await createJob(form)
      navigate(`/recruiter/jobs/${job.id}`)
    } catch (err) {
      setError(err.response?.data?.detail || 'Could not create job.')
    }
  }

  return (
    <div className="max-w-2xl">
      <h1 className="mb-4 text-2xl font-semibold text-slate-900">Create Job</h1>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <input required placeholder="Job title" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })}
          className="rounded-md border border-slate-300 px-3 py-2" />
        <textarea required rows={12} value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })}
          placeholder={'Paste the job description. Use headings like "Required Skills:" and "Preferred Skills:" for best results.'}
          className="rounded-md border border-slate-300 px-3 py-2" />
        {error && <p className="text-sm text-rose-600">{typeof error === 'string' ? error : 'Invalid input'}</p>}
        <button className="rounded-md bg-linear-to-r from-indigo-600 to-violet-600 shadow-md shadow-indigo-500/25 px-4 py-2 text-white">Create job</button>
      </form>
    </div>
  )
}
