function HomePage() {
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
            <p className="feature-card__desc">Przyjmowanie i zarządzanie zgłoszeniami technicznymi</p>
          </div>
          <div className="feature-card">
            <span className="feature-card__icon">🤖</span>
            <h2 className="feature-card__title">Analiza AI</h2>
            <p className="feature-card__desc">Klasyfikacja i nadawanie priorytetu z użyciem AI</p>
          </div>
          <div className="feature-card">
            <span className="feature-card__icon">🔍</span>
            <h2 className="feature-card__title">Podobne przypadki</h2>
            <p className="feature-card__desc">Wyszukiwanie semantycznie podobnych zgłoszeń</p>
          </div>
          <div className="feature-card">
            <span className="feature-card__icon">✉️</span>
            <h2 className="feature-card__title">Import e-mail</h2>
            <p className="feature-card__desc">Automatyczny import zgłoszeń z poczty elektronicznej</p>
          </div>
        </section>

        <div className="status-banner">
          <span className="status-banner__dot" />
          System w trakcie wdrożenia — faza inicjalizacji
        </div>
      </main>

      <footer className="home-footer">
        Praca inżynierska &mdash; Norbert Wrzos &copy; 2025/2026
      </footer>
    </div>
  )
}

export default HomePage
