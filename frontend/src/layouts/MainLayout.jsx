import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import AnimatedBackground from '../components/AnimatedBackground'

export default function MainLayout({ children }) {
  const { user, isAuthenticated, logout } = useAuth()
  const navigate = useNavigate()
  const isLanding = useLocation().pathname === '/'

  const homeLink = user?.role === 'recruiter' ? '/recruiter' : '/candidate'

  function handleLogout() {
    logout()
    navigate('/')
  }

  return (
    <div className={isLanding ? 'min-h-screen bg-slate-50' : 'light-ui relative min-h-screen'}>
      {!isLanding && <AnimatedBackground />}
      <header className="glass sticky top-0 z-50 border-b border-white/60">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <Link to={isAuthenticated ? homeLink : '/'} className="font-display flex items-center gap-2 text-lg font-bold text-slate-900">
            <span className="grid h-8 w-8 place-items-center rounded-xl bg-linear-to-br from-indigo-600 to-fuchsia-500 text-sm text-white shadow-lg shadow-indigo-500/30">M</span>
            <span>Match<span className="gradient-text">IQ</span></span>
          </Link>
          <nav className="flex items-center gap-4 text-sm">
            {isAuthenticated ? (
              <>
                <span className="text-slate-500">
                  {user.name} <span className="rounded bg-slate-100 px-2 py-0.5 text-xs uppercase">{user.role}</span>
                </span>
                <button
                  onClick={handleLogout}
                  className="rounded-md border border-slate-300 px-3 py-1.5 text-slate-700 hover:bg-slate-100"
                >
                  Log out
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="text-slate-600 hover:text-slate-900">
                  Log in
                </Link>
                <Link to="/register" className="rounded-md bg-linear-to-r from-indigo-600 to-violet-600 shadow-md shadow-indigo-500/25 px-3 py-1.5 text-white hover:brightness-110 hover:-translate-y-0.5">
                  Sign up
                </Link>
              </>
            )}
          </nav>
        </div>
      </header>
      <main className={isLanding ? '' : 'relative z-10 mx-auto max-w-6xl px-6 py-10'}>{children}</main>
    </div>
  )
}
