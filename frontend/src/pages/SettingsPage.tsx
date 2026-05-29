import { Link } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'

export default function SettingsPage() {
  const { currentUser } = useAuth()
  const isAdmin = currentUser?.role === 'admin'

  return (
    <div className="page">
      <div className="page__header">
        <h1 className="page__title">Ustawienia</h1>
        <p className="page__subtitle">
          Konfiguracja systemu — widok w przygotowaniu.
        </p>
      </div>

      <div className="mt-6 space-y-4">
        {[
          { title: 'Profil i konto', desc: 'Zarządzanie danymi użytkownika.' },
          { title: 'Powiadomienia', desc: 'Konfiguracja powiadomień e-mail i systemowych.' },
          { title: 'Integracje AI', desc: "Ustawienia pipeline'u analizy i parametry modeli." },
        ].map((item) => (
          <div
            key={item.title}
            className="rounded-xl border border-gray-800 bg-gray-900/60 p-5 flex items-center justify-between"
          >
            <div>
              <div className="text-sm font-medium text-gray-300">{item.title}</div>
              <div className="text-xs text-gray-600 mt-0.5">{item.desc}</div>
            </div>
            <span className="text-xs text-gray-700 border border-gray-800 rounded-full px-2 py-0.5">
              Wkrótce
            </span>
          </div>
        ))}

        {/* Email import — admin only */}
        {isAdmin && (
          <div className="rounded-xl border border-cyan-500/20 bg-gray-900/60 p-5">
            <div className="flex items-start gap-3">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.8} className="w-5 h-5 text-cyan-400 mt-0.5 shrink-0">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                <polyline points="22,6 12,13 2,6"/>
              </svg>
              <div className="flex-1">
                <div className="text-sm font-medium text-cyan-300">Import e-mail</div>
                <p className="text-xs text-gray-500 mt-1 leading-relaxed">
                  Import wiadomości e-mail działa przez backend (IMAP). Zgłoszenia importowane z e-maila
                  pojawiają się na liście zgłoszeń ze źródłem <span className="font-mono text-gray-400">email</span>.
                </p>
                <p className="text-xs text-gray-500 mt-1 leading-relaxed">
                  Aby uruchomić import ręcznie, skorzystaj z{' '}
                  <Link to="/email-import" className="text-cyan-400 hover:text-cyan-300 underline underline-offset-2">
                    panelu importu e-mail
                  </Link>{' '}
                  lub wywołaj endpoint <span className="font-mono text-gray-400">POST /api/email/import</span> przez Swagger.
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
