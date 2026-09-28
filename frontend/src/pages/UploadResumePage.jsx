import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { uploadResume } from '../services/resumeService'

export default function UploadResumePage() {
  const [file, setFile] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  async function handleSubmit(e) {
    e.preventDefault()
    if (!file) return setError('Please choose a PDF or DOCX file.')
    setError('')
    setLoading(true)
    try {
      await uploadResume(file)
      navigate('/candidate/resume')
    } catch (err) {
      setError(err.response?.data?.detail || 'Upload failed.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-lg">
      <h1 className="mb-4 text-2xl font-semibold text-slate-900">Upload Resume</h1>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <input type="file" accept=".pdf,.docx" onChange={(e) => setFile(e.target.files[0])}
          className="rounded-md border border-slate-300 bg-white p-2 text-sm" />
        <p className="text-xs text-slate-500">PDF or DOCX, up to 5MB.</p>
        {error && <p className="text-sm text-rose-600">{error}</p>}
        <button disabled={loading} className="rounded-md bg-linear-to-r from-indigo-600 to-violet-600 shadow-md shadow-indigo-500/25 px-4 py-2 text-white disabled:opacity-50">
          {loading ? 'Uploading...' : 'Upload'}
        </button>
      </form>
    </div>
  )
}
