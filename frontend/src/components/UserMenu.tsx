import { useNavigate } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'

const ROLE_LABELS: Record<string, string> = {
  admin: 'Administrator',
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
    <div className="flex items-center gap-3">
      <div className="text-right hidden sm:block">
        <div className="text-sm font-medium text-gray-200 leading-none">{currentUser.name}</div>
        <div className="text-xs text-gray-500 mt-0.5">
          {ROLE_LABELS[currentUser.role] ?? currentUser.role}
        </div>
      </div>

      <div className="w-8 h-8 rounded-full bg-violet-600 flex items-center justify-center text-xs font-bold text-white flex-shrink-0">
        {initials}
      </div>

      <button
        onClick={handleLogout}
        title="Wyloguj się"
        className="p-1.5 text-gray-500 hover:text-gray-200 hover:bg-gray-800 rounded-lg transition-colors"
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
