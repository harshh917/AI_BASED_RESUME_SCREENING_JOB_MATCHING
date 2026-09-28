import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { getMatchDetail, getResume } from '../services/resumeService'
import ScoreBadge from '../components/ScoreBadge'
import SkillList from '../components/SkillList'

export default function MatchDetailsPage() {
  const { jobId, resumeId } = useParams()
  const [match, setMatch] = useState(null)
  const [resume, setResume] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    getMatchDetail(jobId, resumeId).then(setMatch).catch((e) => setError(e.response?.data?.detail || 'Failed to load'))
    getResume(resumeId).then(setResume).catch(() => {})
  }, [jobId, resumeId])

  if (error) return <p className="text-rose-600">{error}</p>
  if (!match) return <p className="text-slate-500">Loading...</p>
  const name = resume?.profile?.summary?.split('\n')[0] || 'Candidate'
  const projects = resume?.profile?.projects || []
  const experience = resume?.profile?.experience || []

  return (
    <div className="flex flex-col gap-6">
      <Link to={`/recruiter/jobs/${jobId}`} className="text-sm underline">← Back to ranking</Link>
      <h1 className="text-2xl font-semibold text-slate-900">{name}</h1>
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-6">
        <ScoreBadge label="Overall" score={match.overall_score} />
        <ScoreBadge label="Skills" score={match.skill_score} />
        <ScoreBadge label="Semantic" score={match.semantic_score} />
        <ScoreBadge label="Experience" score={match.experience_score} />
        <ScoreBadge label="Education" score={match.education_score} />
        <ScoreBadge label="Projects" score={match.project_score} />
      </div>
      <SkillList title="Matched skills" skills={match.matched_skills} variant="matched" />
      <SkillList title="Missing / unclear (required)" skills={match.missing_skills} variant="neutral" emptyText="None — all required skills were found" />
      <div>
        <h3 className="mb-2 text-sm font-semibold text-slate-800">Relevant experience</h3>
        {experience.length ? <ul className="list-disc pl-5 text-sm">{experience.map((e, i) => <li key={i}>{e.role} @ {e.company} ({e.duration || 'duration not identified'})</li>)}</ul>
          : <p className="text-sm text-slate-500">Not identified in the submitted resume</p>}
      </div>
      <div>
        <h3 className="mb-2 text-sm font-semibold text-slate-800">Relevant projects</h3>
        {projects.length ? <ul className="list-disc pl-5 text-sm">{projects.map((p, i) => <li key={i}>{p.name}</li>)}</ul>
          : <p className="text-sm text-slate-500">Not identified in the submitted resume</p>}
      </div>
      <div>
        <h3 className="mb-2 text-sm font-semibold text-slate-800">Match explanation</h3>
        <pre className="whitespace-pre-wrap rounded-2xl border border-white bg-white/85 shadow-sm backdrop-blur p-4 text-sm text-slate-700">{match.explanation}</pre>
      </div>
      <p className="text-xs text-slate-500">Semantic similarity is only one signal; this tool supports, not replaces, human review.</p>
    </div>
  )
}
