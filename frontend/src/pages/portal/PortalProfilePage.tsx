import { useNavigate } from 'react-router-dom'
import { useAuth } from '../../auth/AuthContext'
import PortalLayout from '../../components/PortalLayout'
import type { UserRole } from '../../types/auth'

const ROLE_LABELS: Record<UserRole, string> = {
  agent: 'Agent IT',
  end_user: 'Użytkownik',
}

export default function PortalProfilePage() {
  const { currentUser, logout } = useAuth()
  const navigate = useNavigate()

  if (!currentUser) return null

  function handleLogout() {
    logout()
    navigate('/login')
  }

  return (
    <PortalLayout>
      <div className="page max-w-2xl">
        <div className="page__header">
          <h1 className="page__title">Profil</h1>
          <p className="page__subtitle">Informacje o Twoim koncie.</p>
        </div>

        <div className="surface-card surface-card--soft space-y-6 p-6">
          {/* Avatar */}
          <div className="flex items-center gap-4">
            <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-violet-600 text-2xl font-bold text-white shadow-sm">
              {currentUser.name.charAt(0).toUpperCase()}
            </div>
            <div>
              <p className="text-lg font-semibold text-gray-100">{currentUser.name}</p>
              <p className="text-sm text-gray-500">{ROLE_LABELS[currentUser.role] ?? currentUser.role}</p>
            </div>
          </div>

          {/* Details */}
          <dl className="space-y-3 rounded-2xl border border-white/10 bg-white/[0.03] p-4">
            <div className="flex gap-3 text-sm">
              <dt className="text-gray-500 w-28 shrink-0">E-mail</dt>
              <dd className="text-gray-300 break-all">{currentUser.email}</dd>
            </div>
            <div className="flex gap-3 text-sm">
              <dt className="text-gray-500 w-28 shrink-0">Rola</dt>
              <dd className="text-gray-300">{ROLE_LABELS[currentUser.role] ?? currentUser.role}</dd>
            </div>
            <div className="flex gap-3 text-sm">
              <dt className="text-gray-500 w-28 shrink-0">ID konta</dt>
              <dd className="text-gray-600 font-mono text-xs">{currentUser.id}</dd>
            </div>
          </dl>

          {/* Notice */}
          <div className="rounded-2xl border border-white/10 bg-white/[0.02] px-4 py-3 text-xs text-gray-500">
            To jest konto mockowe używane w celach demonstracyjnych. Dane są statyczne.
          </div>

          {/* Logout */}
          <button
            onClick={handleLogout}
            className="inline-flex items-center gap-2 rounded-full border border-red-500/20 bg-red-500/10 px-4 py-2 text-sm font-medium text-red-300 transition-colors hover:bg-red-500/15 hover:text-red-200"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.8} className="w-4 h-4">
              <path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4" />
              <polyline points="16 17 21 12 16 7" />
              <line x1="21" y1="12" x2="9" y2="12" />
            </svg>
            Wyloguj się
          </button>
        </div>
      </div>
    </PortalLayout>
  )
}
