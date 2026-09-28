import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { listResumes, getResume, viewResume } from '../services/resumeService'
import SkillList from '../components/SkillList'

export default function MyResumePage() {
  const [resume, setResume] = useState(null)
  const [loading, setLoading] = useState(true)
  useEffect(() => {
    listResumes()
      .then((items) => (items.length ? getResume(items[0].id) : null))
      .then(setResume)
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <p className="text-slate-500">Loading...</p>
  if (!resume) return (
    <p className="text-slate-600">No resume yet. <Link className="underline" to="/candidate/upload">Upload one</Link>.</p>
  )
  const skills = resume.profile?.skills || {}
  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <h1 className="text-2xl font-semibold text-slate-900">My Resume: {resume.file_name}</h1>
        <button type="button" onClick={() => viewResume(resume.id)} className="rounded-md border border-indigo-200 bg-indigo-50 px-4 py-2 text-sm font-medium text-indigo-700 hover:bg-indigo-100">
          View Resume ↗
        </button>
      </div>
      {Object.entries(skills).map(([cat, list]) => list.length > 0 && (
        <SkillList key={cat} title={cat.replace('_', ' ')} skills={list} variant="matched" />
      ))}
      <Section title="Education" items={resume.profile?.education?.map((e) => `${e.degree || ''} — ${e.institution || ''} ${e.graduation_year || ''}`)} />
      <Section title="Experience" items={resume.profile?.experience?.map((e) => `${e.role || ''} @ ${e.company || ''} (${e.duration || 'duration not identified'})`)} />
      <Section title="Projects" items={resume.profile?.projects?.map((p) => p.name)} />
      <Section title="Certifications" items={resume.profile?.certifications} />
    </div>
  )
}

function Section({ title, items }) {
  return (
    <div>
      <h3 className="mb-2 text-sm font-semibold text-slate-800">{title}</h3>
      {items && items.length ? (
        <ul className="list-disc pl-5 text-sm text-slate-700">{items.map((i, idx) => <li key={idx}>{i}</li>)}</ul>
      ) : <p className="text-sm text-slate-500">Not identified in the submitted resume</p>}
    </div>
  )
}
