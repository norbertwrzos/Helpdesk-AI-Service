import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'
import { MOCK_USERS } from '../auth/mockUsers'
import type { UserRole } from '../types/auth'

const ROLE_LABELS: Record<UserRole, string> = {
  admin: 'Administrator',
  agent: 'Agent IT Support',
  end_user: 'Użytkownik końcowy',
}

export default function LoginPage() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [selectedUserId, setSelectedUserId] = useState(MOCK_USERS[0].id)

  function handleLogin(e: React.FormEvent) {
    e.preventDefault()
    login(selectedUserId)
    const user = MOCK_USERS.find(u => u.id === selectedUserId)
    if (user?.role === 'end_user') {
      navigate('/portal')
    } else {
      navigate('/')
    }
  }

  return (
    <div className="login-page">
      <div className="login-card">
        <h1 className="login-card__title">Helpdesk AI Service</h1>
        <p className="login-card__subtitle">
          Logowanie demonstracyjne — wybierz użytkownika
        </p>

        <form onSubmit={handleLogin}>
          <div className="form-group">
            <label className="form-label" htmlFor="user-select">
              Użytkownik / rola
            </label>
            <select
              id="user-select"
              className="form-input"
              value={selectedUserId}
              onChange={e => setSelectedUserId(e.target.value)}
            >
              {MOCK_USERS.map(u => (
                <option key={u.id} value={u.id}>
                  {u.name} — {u.email} ({ROLE_LABELS[u.role]})
                </option>
              ))}
            </select>
          </div>

          <button type="submit" className="btn btn--primary btn--full">
            Zaloguj się
          </button>
        </form>

        <p className="login-card__notice">
          To jest prototyp. Logowanie jest mockowe i służy do demonstracji ról.
        </p>
      </div>
    </div>
  )
}
