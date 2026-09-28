import { useEffect, useState } from 'react'
import { listJobs, listResumes, getResume } from '../services/resumeService'

export default function DataExplorerPage() {
  const [resumes, setResumes] = useState([])
  const [jobs, setJobs] = useState([])
  const [selected, setSelected] = useState(null)
  const [error, setError] = useState('')
  useEffect(() => {
    Promise.all([listResumes(), listJobs()]).then(([rs, js]) => { setResumes(rs); setJobs(js) }).catch(e => setError(e.response?.data?.detail || 'Could not load data.'))
  }, [])
  async function inspect(id) {
    try { setSelected(await getResume(id)) } catch (e) { setError(e.response?.data?.detail || 'Could not load resume profile.') }
  }
  const skills = selected?.profile?.skills ? Object.values(selected.profile.skills).flat() : []
  return (
    <div className="flex flex-col gap-6">
      <div><h1 className="text-2xl font-semibold text-slate-900">Dataset Explorer</h1><p className="mt-1 text-sm text-slate-500">View the actual resumes and job descriptions stored in this application.</p></div>
      {error && <p className="text-sm text-rose-600">{error}</p>}
      <div className="grid gap-4 lg:grid-cols-2">
        <section className="rounded-2xl border border-white bg-white/85 p-5 shadow-sm">
          <h2 className="font-semibold text-slate-900">Uploaded resumes <span className="text-sm font-normal text-slate-500">({resumes.length})</span></h2>
          <div className="mt-3 divide-y divide-slate-100">{resumes.map(r => <button key={r.id} onClick={() => inspect(r.id)} className="flex w-full items-center justify-between py-3 text-left hover:bg-slate-50"><span className="truncate text-sm text-slate-800">{r.file_name}</span><span className="text-xs text-indigo-600">Inspect →</span></button>)}{!resumes.length && <p className="py-4 text-sm text-slate-500">No uploaded resumes.</p>}</div>
        </section>
        <section className="rounded-2xl border border-white bg-white/85 p-5 shadow-sm">
          <h2 className="font-semibold text-slate-900">Job descriptions <span className="text-sm font-normal text-slate-500">({jobs.length})</span></h2>
          <div className="mt-3 divide-y divide-slate-100">{jobs.map(j => <div key={j.id} className="py-3"><div className="flex items-center justify-between"><span className="font-medium text-sm text-slate-800">{j.title}</span><span className="text-xs text-slate-500">{j.status || 'active'}</span></div><p className="mt-1 line-clamp-2 text-xs text-slate-500">{j.description}</p></div>)}{!jobs.length && <p className="py-4 text-sm text-slate-500">No jobs available.</p>}</div>
        </section>
      </div>
      {selected && <section className="rounded-2xl border border-white bg-white/85 p-5 shadow-sm">
        <div className="flex items-center justify-between"><div><h2 className="font-semibold text-slate-900">{selected.file_name}</h2><p className="text-xs text-slate-500">Parsed candidate profile</p></div><span className="rounded-full bg-indigo-50 px-3 py-1 text-xs font-medium text-indigo-700">Parsed</span></div>
        <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <div><p className="text-xs text-slate-500">Skills</p><p className="mt-1 text-sm">{skills.length ? skills.join(', ') : 'Not identified'}</p></div>
          <div><p className="text-xs text-slate-500">Education</p><p className="mt-1 text-sm">{selected.profile?.education?.length || 0} entries</p></div>
          <div><p className="text-xs text-slate-500">Experience</p><p className="mt-1 text-sm">{selected.profile?.experience?.length || 0} entries</p></div>
          <div><p className="text-xs text-slate-500">Projects</p><p className="mt-1 text-sm">{selected.profile?.projects?.length || 0} entries</p></div>
        </div>
      </section>}
    </div>
  )
}
