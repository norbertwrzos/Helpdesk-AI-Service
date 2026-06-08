import type { MockUser, UserRole } from '../../types/auth'

const ROLE_LABELS: Record<UserRole, string> = {
  agent: 'Agent',
  end_user: 'Użytkownik',
}

const ROLE_COLORS: Record<UserRole, string> = {
  agent: 'text-cyan-400 border-cyan-700',
  end_user: 'text-gray-400 border-gray-700',
}

interface Props {
  user: MockUser
  onLogout: () => void
}

export default function MockUserSettings({ user, onLogout }: Props) {
  const roleColor = ROLE_COLORS[user.role]

  return (
    <div className="rounded-xl border border-gray-800 bg-gray-900/60 p-5 space-y-5">
      <h3 className="text-sm font-semibold text-gray-200">Profil użytkownika</h3>

      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-xs text-gray-500">Imię</span>
          <span className="text-sm text-gray-200">{user.name}</span>
        </div>
        <div className="flex items-center justify-between">
          <span className="text-xs text-gray-500">E-mail</span>
          <span className="text-sm text-gray-300 font-mono">{user.email}</span>
        </div>
        <div className="flex items-center justify-between">
          <span className="text-xs text-gray-500">Rola</span>
          <span className={`text-xs border rounded-full px-2 py-0.5 ${roleColor}`}>
            {ROLE_LABELS[user.role] ?? user.role}
          </span>
        </div>
        <div className="flex items-center justify-between">
          <span className="text-xs text-gray-500">ID</span>
          <span className="text-xs text-gray-600 font-mono">{user.id}</span>
        </div>
      </div>

      <div className="pt-2 border-t border-gray-800">
        <p className="text-xs text-gray-600 mb-3">
          To jest środowisko testowe z mockowym uwierzytelnianiem.
        </p>
        <button
          onClick={onLogout}
          className="px-4 py-2 rounded-lg border border-red-700/60 text-red-400 hover:bg-red-900/20 text-sm font-medium transition-colors"
        >
          Wyloguj
        </button>
      </div>
    </div>
  )
}
