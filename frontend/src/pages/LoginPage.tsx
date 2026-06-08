import { useState } from 'react'
import { Navigate, useNavigate } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'
import { MOCK_USERS } from '../auth/mockUsers'
import type { UserRole } from '../types/auth'

const ROLE_LABELS: Record<UserRole, string> = {
  agent: 'Agent',
  end_user: 'Użytkownik końcowy',
}

const ROLE_DESCRIPTIONS: Record<UserRole, string> = {
  agent: 'Panel do obsługi zgłoszeń, ustawień, klasyfikacji oraz odpowiedzi AI dla klientów.',
  end_user: 'Portal do zgłaszania problemów, śledzenia statusów i kontaktu z działem wsparcia.',
}

const ROLE_DESTINATIONS: Record<UserRole, string> = {
  agent: 'Panel agenta i ustawienia',
  end_user: 'Portal użytkownika z listą zgłoszeń',
}

const LOGIN_FEATURES = [
  {
    title: 'Obsługa zgłoszeń',
    description: 'Przegląd ticketów, priorytetów i kategorii w jednym miejscu.',
  },
  {
    title: 'Wsparcie AI',
    description: 'Generowanie odpowiedzi i ocena jakości bez opuszczania panelu.',
  },
  {
    title: 'Portal użytkownika',
    description: 'Szybkie zgłoszenia, historia spraw i prosty kontakt z działem wsparcia.',
  },
] as const

function getRedirectPath(role: UserRole) {
  return role === 'end_user' ? '/portal/tickets' : '/dashboard'
}

export default function LoginPage() {
  const { currentUser, login } = useAuth()
  const navigate = useNavigate()
  const [selectedUserId, setSelectedUserId] = useState(MOCK_USERS[0].id)
  const selectedUser = MOCK_USERS.find(user => user.id === selectedUserId) ?? MOCK_USERS[0]

  if (currentUser) {
    return <Navigate to={getRedirectPath(currentUser.role)} replace />
  }

  function handleLogin(e: React.FormEvent) {
    e.preventDefault()
    login(selectedUser.id)
    navigate(getRedirectPath(selectedUser.role))
  }

  return (
    <main className="login-page">
      <div className="login-layout">
        <section className="login-card" aria-labelledby="login-title">
          <div className="login-card__header">
            <p className="section-heading">Dostęp demo</p>
            <h1 id="login-title" className="login-card__title">
              Zaloguj się do Helpdesk AI Service
            </h1>
            <p className="login-card__subtitle">
              Wybierz konto testowe, aby przejść do panelu agenta lub portalu użytkownika.
            </p>
          </div>

          <form onSubmit={handleLogin} className="login-form">
            <fieldset className="login-user-picker">
              <legend className="form-label">Konto testowe</legend>

              <div className="login-user-list">
                {MOCK_USERS.map(user => {
                  const isActive = user.id === selectedUser.id

                  return (
                    <button
                      key={user.id}
                      type="button"
                      className={`login-user-option${isActive ? ' login-user-option--active' : ''}`}
                      onClick={() => setSelectedUserId(user.id)}
                      aria-pressed={isActive}
                    >
                      <span className="login-user-option__header">
                        <span className="login-user-option__name">{user.name}</span>
                        <span className={`login-role-badge login-role-badge--${user.role}`}>
                          {ROLE_LABELS[user.role]}
                        </span>
                      </span>
                      <span className="login-user-option__email">{user.email}</span>
                      <span className="login-user-option__meta">{ROLE_DESCRIPTIONS[user.role]}</span>
                    </button>
                  )
                })}
              </div>
            </fieldset>

            <div className="login-selected-user">
              <p className="login-selected-user__label">Po zalogowaniu trafisz do</p>
              <p className="login-selected-user__destination">{ROLE_DESTINATIONS[selectedUser.role]}</p>
              <p className="login-selected-user__hint">{ROLE_DESCRIPTIONS[selectedUser.role]}</p>
            </div>

            <button type="submit" className="btn btn--primary login-card__submit">
              Zaloguj się jako {selectedUser.name}
            </button>
          </form>

          <p className="login-card__notice">
            To jest prototyp. Logowanie jest mockowe i służy do demonstracji dwóch profili oraz przepływów w aplikacji.
          </p>
        </section>

        <aside className="login-hero" aria-label="Informacje o aplikacji">
          <div className="login-hero__intro">
            <span className="login-hero__badge">Środowisko testowe</span>
            <h2 className="login-hero__title">
              Jedno miejsce do obsługi zgłoszeń, wiedzy i odpowiedzi AI.
            </h2>
            <p className="login-hero__subtitle">
              Ten ekran pozwala szybko przełączać profile i sprawdzać pełne ścieżki produktu bez prawdziwej autoryzacji.
            </p>
          </div>

          <div className="login-hero__grid">
            {LOGIN_FEATURES.map(feature => (
              <article key={feature.title} className="login-feature-card">
                <h3 className="login-feature-card__title">{feature.title}</h3>
                <p className="login-feature-card__description">{feature.description}</p>
              </article>
            ))}
          </div>
        </aside>
      </div>
    </main>
  )
}
