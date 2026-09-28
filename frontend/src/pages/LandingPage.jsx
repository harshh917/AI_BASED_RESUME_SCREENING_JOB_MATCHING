import { Link } from 'react-router-dom'
import { CountUp, Reveal } from '../hooks/useReveal'
import ScoreBadge from '../components/ScoreBadge'

const SKILLS = ['Python', 'Java', 'React', 'Spring Boot', 'PostgreSQL', 'Docker', 'AWS', 'FastAPI', 'Kubernetes', 'TypeScript', 'Node.js', 'Machine Learning', 'NLP', 'REST API', 'Git', 'MongoDB', 'Django', 'Terraform']
const ROLES = ['Backend Developer', 'Frontend Developer', 'Data Scientist', 'DevOps Engineer']

export default function LandingPage() {
  return (
    <div className="overflow-hidden">
      {/* HERO */}
      <section className="relative px-6 pb-24 pt-20">
        <div className="animate-blob absolute -left-24 top-0 h-96 w-96 rounded-full bg-indigo-400/30 blur-3xl" />
        <div className="animate-blob absolute right-0 top-32 h-96 w-96 rounded-full bg-fuchsia-400/25 blur-3xl [animation-delay:-5s]" />
        <div className="relative mx-auto grid max-w-6xl items-center gap-12 lg:grid-cols-2">
          <div>
            <span className="animate-pop inline-flex items-center gap-2 rounded-full border border-indigo-200 bg-white/80 px-4 py-1.5 text-sm font-semibold text-indigo-700 shadow-sm">
              <span className="h-2 w-2 animate-pulse rounded-full bg-emerald-500" /> Explainable AI hiring assistant
            </span>
            <h1 className="mt-6 text-5xl font-extrabold leading-[1.08] text-slate-900 xl:text-6xl">
              Find the right hire.<br /><span className="gradient-text">Skip the guesswork.</span>
            </h1>
            <p className="mt-6 max-w-xl text-lg text-slate-600">
              Upload resumes, paste a job description, and get a ranked shortlist where every score shows its reasons.
              Skills, semantics and experience are compared — never gender, age, religion or photos.
            </p>

            {/* search-style bar */}
            <Link to="/register" className="group mt-8 flex max-w-xl items-center gap-3 rounded-2xl border border-white bg-white p-2 pl-5 shadow-xl shadow-indigo-500/10 hover:shadow-indigo-500/25">
              <span className="text-slate-400">🔍</span>
              <span className="flex-1 truncate text-slate-400">Paste a job description to screen candidates…</span>
              <span className="rounded-xl bg-linear-to-r from-indigo-600 to-fuchsia-600 px-5 py-3 text-sm font-semibold text-white group-hover:brightness-110">Screen now →</span>
            </Link>
            <div className="mt-4 flex flex-wrap gap-2 text-sm text-slate-500">
              Popular roles:
              {ROLES.map((r) => <span key={r} className="rounded-full bg-white/80 px-3 py-1 font-medium text-slate-700 shadow-sm">{r}</span>)}
            </div>
          </div>

          {/* floating sample cards */}
          <div className="relative mx-auto h-[420px] w-full max-w-md">
            <div className="animate-float glass absolute left-0 top-4 w-72 rounded-3xl p-5 shadow-2xl shadow-indigo-500/20">
              <div className="flex items-center gap-4">
                <ScoreBadge score={87} size={84} />
                <div>
                  <p className="font-display font-bold text-slate-900">Sample Candidate</p>
                  <p className="text-xs text-slate-500">Backend Developer · illustrative</p>
                </div>
              </div>
              <div className="mt-4 flex flex-wrap gap-2">
                {['Java', 'Spring Boot', 'PostgreSQL'].map((s) => <span key={s} className="rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700">✓ {s}</span>)}
                <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-500">○ Docker</span>
              </div>
            </div>
            <div className="animate-float-slow glass absolute bottom-6 right-0 w-64 rounded-3xl p-5 shadow-2xl shadow-fuchsia-500/20 [--r:3deg]">
              <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">Why this score?</p>
              <p className="mt-2 text-sm text-slate-700">Strong alignment on required skills. Docker was <b>not identified</b> in the submitted resume.</p>
              <div className="mt-3 h-2 overflow-hidden rounded-full bg-slate-200"><div className="h-full w-[87%] rounded-full bg-linear-to-r from-indigo-500 to-fuchsia-500" /></div>
            </div>
            <div className="animate-float glass absolute right-6 top-0 rounded-2xl px-4 py-2 text-sm font-semibold text-indigo-700 shadow-lg [--r:-4deg]">🏆 Rank #1</div>
          </div>
        </div>
      </section>

      {/* SKILL MARQUEE */}
      <section className="border-y border-white/70 bg-white/60 py-5 backdrop-blur">
        <div className="flex w-max animate-marquee gap-4">
          {[...SKILLS, ...SKILLS].map((s, i) => <span key={i} className="rounded-full border border-indigo-100 bg-white px-5 py-2 font-semibold text-slate-700 shadow-sm">{s}</span>)}
        </div>
      </section>

      {/* STATS (facts about the system, not usage claims) */}
      <section className="mx-auto grid max-w-6xl grid-cols-2 gap-6 px-6 py-20 text-center lg:grid-cols-4">
        {[[6, '', 'matching signals'], [0, '', 'protected attributes used'], [2, '', 'file formats: PDF, DOCX'], [100, '%', 'explained scores']].map(([n, suf, label], i) => (
          <Reveal key={label} delay={i * 100}>
            <p className="font-display text-5xl font-extrabold gradient-text"><CountUp to={n} suffix={suf} /></p>
            <p className="mt-2 text-sm font-medium text-slate-500">{label}</p>
          </Reveal>
        ))}
      </section>

      {/* HOW IT WORKS */}
      <section className="mx-auto max-w-6xl px-6 pb-20">
        <Reveal><h2 className="text-center text-4xl font-bold">From resume to <span className="gradient-text">ranked shortlist</span></h2></Reveal>
        <div className="mt-12 grid gap-6 md:grid-cols-3">
          {[['📄', 'Upload', 'PDF or DOCX resumes are parsed into skills, education, experience and projects.'],
            ['🧠', 'Match', 'Skill coverage, semantic similarity, experience, projects and more are combined into one score.'],
            ['💡', 'Understand', 'Each result explains matched skills, gaps and what could not be identified.']].map(([icon, t, d], i) => (
            <Reveal key={t} delay={i * 120}>
              <div className="card-lift h-full rounded-3xl border border-white bg-white/85 p-7 shadow-sm">
                <div className="grid h-14 w-14 place-items-center rounded-2xl bg-linear-to-br from-indigo-100 to-fuchsia-100 text-2xl">{icon}</div>
                <p className="font-display mt-1 text-sm font-bold text-indigo-500">0{i + 1}</p>
                <h3 className="text-xl font-bold">{t}</h3>
                <p className="mt-2 text-slate-600">{d}</p>
              </div>
            </Reveal>
          ))}
        </div>
      </section>

      {/* AUDIENCES */}
      <section className="mx-auto grid max-w-6xl gap-6 px-6 pb-24 md:grid-cols-2">
        <Reveal><Audience tone="from-indigo-600 to-violet-600" title="For recruiters" points={['Ranked candidate table with filters', 'Per-candidate score breakdown', 'Configurable scoring weights']} cta="Start screening" /></Reveal>
        <Reveal delay={150}><Audience tone="from-fuchsia-600 to-rose-500" title="For candidates" points={['Upload once, see your parsed profile', 'Browse open roles and required skills', 'Your data is only visible to you and authorised recruiters']} cta="Upload resume" /></Reveal>
      </section>

      <footer className="border-t border-white/70 py-8 text-center text-sm text-slate-500">
        MatchIQ is a decision-support tool. Humans make hiring decisions. · Final-year CSE project
      </footer>
    </div>
  )
}

function Audience({ tone, title, points, cta }) {
  return (
    <div className={`card-lift relative h-full overflow-hidden rounded-3xl bg-linear-to-br ${tone} p-8 text-white shadow-xl`}>
      <div className="absolute -right-10 -top-10 h-44 w-44 rounded-full bg-white/15 blur-2xl" />
      <h3 className="text-2xl font-bold">{title}</h3>
      <ul className="mt-4 space-y-2 text-white/90">{points.map((p) => <li key={p}>✓ {p}</li>)}</ul>
      <Link to="/register" className="mt-6 inline-block rounded-xl bg-white px-5 py-2.5 font-semibold text-slate-900 hover:-translate-y-0.5">{cta} →</Link>
    </div>
  )
}
