import { useNavigate } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'

export default function NotFoundPage() {
  const navigate = useNavigate()
  const { role } = useAuth()

  function goHome() {
    if (role === 'end_user') {
      navigate('/portal/tickets')
    } else if (role) {
      navigate('/dashboard')
    } else {
      navigate('/login')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center" style={{ background: 'var(--color-bg)' }}>
      <div className="text-center space-y-5 max-w-sm px-6">
        <div className="text-7xl font-bold text-gray-800">404</div>
        <h1 className="text-xl font-semibold text-gray-200">Strona nie istnieje</h1>
        <p className="text-sm text-gray-500">
          Żądana strona nie została znaleziona lub nie masz do niej dostępu.
        </p>
        <button
          onClick={goHome}
          className="inline-flex items-center gap-2 bg-violet-600 hover:bg-violet-500 text-white text-sm font-medium px-5 py-2.5 rounded-lg transition-colors"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-4 h-4">
            <line x1="19" y1="12" x2="5" y2="12" />
            <polyline points="12 19 5 12 12 5" />
          </svg>
          Wróć do strony głównej
        </button>
      </div>
    </div>
  )
}
