import { useNavigate } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'
import type { UserRole } from '../types/auth'

const ROLE_LABELS: Record<UserRole, string> = {
  agent: 'Agent IT',
  end_user: 'Użytkownik',
}

export default function UserMenu() {
  const { currentUser, logout } = useAuth()
  const navigate = useNavigate()

  if (!currentUser) return null

  const initials = currentUser.name
    .split(' ')
    .map((p) => p[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)

  function handleLogout() {
    logout()
    navigate('/login')
  }

  return (
    <div className="flex items-center gap-2 rounded-full border border-white/10 bg-white/[0.04] py-1 pl-2 pr-1">
      <div className="hidden text-right sm:block">
        <div className="text-sm font-medium leading-none text-slate-100">{currentUser.name}</div>
        <div className="mt-0.5 text-xs text-slate-500">
          {ROLE_LABELS[currentUser.role] ?? currentUser.role}
        </div>
      </div>

      <div className="flex h-9 w-9 flex-shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-violet-500 to-cyan-400 text-xs font-bold text-white shadow-[0_12px_24px_rgba(99,102,241,0.3)]">
        {initials}
      </div>

      <button
        onClick={handleLogout}
        title="Wyloguj się"
        className="rounded-full p-2 text-slate-500 transition-colors hover:bg-white/5 hover:text-slate-100"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.8} className="w-5 h-5">
          <path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4" />
          <polyline points="16 17 21 12 16 7" />
          <line x1="21" y1="12" x2="9" y2="12" />
        </svg>
      </button>
    </div>
  )
}
