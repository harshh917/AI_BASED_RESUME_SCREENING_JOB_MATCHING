import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'

export default function RegisterPage() {
  const { register } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({ name: '', email: '', password: '', role: 'candidate' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const data = await register(form)
      navigate(data.user.role === 'recruiter' ? '/recruiter' : '/candidate')
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="glass mx-auto mt-8 max-w-md rounded-3xl p-8 shadow-xl animate-pop">
      <h1 className="mb-6 text-2xl font-semibold text-slate-900">Create your account</h1>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <Field label="Full name" value={form.name} onChange={(v) => setForm({ ...form, name: v })} />
        <Field label="Email" type="email" value={form.email} onChange={(v) => setForm({ ...form, email: v })} />
        <Field
          label="Password (min 8 characters)"
          type="password"
          value={form.password}
          onChange={(v) => setForm({ ...form, password: v })}
        />
        <label className="flex flex-col gap-1 text-sm text-slate-700">
          I am a...
          <select
            value={form.role}
            onChange={(e) => setForm({ ...form, role: e.target.value })}
            className="rounded-md border border-slate-300 px-3 py-2"
          >
            <option value="candidate">Candidate</option>
            <option value="recruiter">Recruiter</option>
          </select>
        </label>
        {error && <p className="text-sm text-rose-600">{error}</p>}
        <button
          type="submit"
          disabled={loading}
          className="rounded-md bg-linear-to-r from-indigo-600 to-violet-600 shadow-md shadow-indigo-500/25 px-4 py-2 text-white hover:brightness-110 hover:-translate-y-0.5 disabled:opacity-50"
        >
          {loading ? 'Creating account...' : 'Sign up'}
        </button>
      </form>
      <p className="mt-4 text-sm text-slate-600">
        Already have an account?{' '}
        <Link to="/login" className="font-medium text-slate-900 underline">
          Log in
        </Link>
      </p>
    </div>
  )
}

function Field({ label, type = 'text', value, onChange }) {
  return (
    <label className="flex flex-col gap-1 text-sm text-slate-700">
      {label}
      <input
        type={type}
        required
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="rounded-md border border-slate-300 px-3 py-2 focus:border-slate-500 focus:outline-none"
      />
    </label>
  )
}
