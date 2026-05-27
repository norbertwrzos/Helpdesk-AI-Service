import { Link } from 'react-router-dom'

export default function HomePage() {
  return (
    <div className="home-page">
      <header className="home-header">
        <div className="home-header__badge">AI-Powered Support</div>
        <h1 className="home-header__title">Helpdesk AI Service</h1>
        <p className="home-header__subtitle">
          Zautomatyzowany system obsługi zgłoszeń technicznych wspomagany przez sztuczną inteligencję
        </p>
      </header>

      <main className="home-main">
        <section className="feature-grid">
          <div className="feature-card">
            <span className="feature-card__icon">📋</span>
            <h2 className="feature-card__title">Zgłoszenia</h2>
            <p className="feature-card__desc">Przyjmowanie i zarządzanie zgłoszeniami technicznymi z kategoriami i priorytetami</p>
          </div>
          <div className="feature-card">
            <span className="feature-card__icon">🏷️</span>
            <h2 className="feature-card__title">Kategorie i priorytety</h2>
            <p className="feature-card__desc">Organizacja zgłoszeń według kategorii problemu i poziomu pilności</p>
          </div>
          <div className="feature-card">
            <span className="feature-card__icon">🤖</span>
            <h2 className="feature-card__title">Analiza AI</h2>
            <p className="feature-card__desc">Klasyfikacja, priorytetyzacja i propozycje rozwiązań z użyciem AI/NLP — w przygotowaniu</p>
          </div>
          <div className="feature-card">
            <span className="feature-card__icon">✉️</span>
            <h2 className="feature-card__title">Import e-mail</h2>
            <p className="feature-card__desc">Automatyczny import zgłoszeń z poczty elektronicznej — w przygotowaniu</p>
          </div>
        </section>

        <div className="status-banner">
          <span className="status-banner__dot" />
          Etap 2 — obsługa zgłoszeń, kategorie i priorytety. Moduły AI i import e-mail będą realizowane w kolejnych etapach.
        </div>

        <div className="home-cta">
          <Link to="/tickets" className="btn btn--primary btn--lg">
            Przejdź do zgłoszeń →
          </Link>
        </div>
      </main>

      <footer className="home-footer">
        Praca inżynierska &mdash; Norbert Wrzos &copy; 2025/2026
      </footer>
    </div>
  )
}

