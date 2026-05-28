export default function SettingsPage() {
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
          { title: 'Import e-mail', desc: 'Konfiguracja serwera IMAP i harmonogramu importu.' },
          { title: 'Integracje AI', desc: 'Ustawienia pipeline\'u analizy i parametry modeli.' },
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
      </div>
    </div>
  )
}
