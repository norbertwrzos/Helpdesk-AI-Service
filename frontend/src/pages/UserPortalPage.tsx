import { useAuth } from '../auth/AuthContext'

/**
 * Uproszczony portal dla użytkownika końcowego (end_user).
 * Etap 6: placeholder — pełna implementacja w kolejnym etapie.
 */
export default function UserPortalPage() {
  const { currentUser, logout } = useAuth()

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Portal zgłoszeń</h1>
      <p>Witaj, {currentUser?.name}! Tu możesz zgłaszać problemy i śledzić status swoich zgłoszeń.</p>
      <button className="btn btn--secondary" onClick={logout}>
        Wyloguj się
      </button>
    </div>
  )
}
