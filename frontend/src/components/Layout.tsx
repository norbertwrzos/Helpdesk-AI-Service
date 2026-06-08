import { NavLink } from 'react-router-dom'

interface LayoutProps {
  children: React.ReactNode
}

export default function Layout({ children }: LayoutProps) {
  return (
    <div className="layout">
      <header className="layout__header">
        <div className="layout__header-inner">
          <div className="layout__brand">
            <span className="layout__brand-icon">🛠</span>
            <div>
              <div className="layout__brand-title">Helpdesk AI Service</div>
              <div className="layout__brand-sub">
                Serwis wspierający obsługę zgłoszeń technicznych z wykorzystaniem metod AI/NLP
              </div>
            </div>
          </div>
          <nav className="layout__nav">
            <NavLink to="/" end className={({ isActive }) => 'layout__nav-link' + (isActive ? ' active' : '')}>
              Home
            </NavLink>
            <NavLink to="/tickets" className={({ isActive }) => 'layout__nav-link' + (isActive ? ' active' : '')}>
              Zgłoszenia
            </NavLink>
            <NavLink to="/quality" className={({ isActive }) => 'layout__nav-link' + (isActive ? ' active' : '')}>
              Jakość AI
            </NavLink>
          </nav>
        </div>
      </header>
      <main className="layout__content">{children}</main>
      <footer className="layout__footer">
        Praca inżynierska &mdash; Norbert Wrzos &copy; 2025/2026
      </footer>
    </div>
  )
}
