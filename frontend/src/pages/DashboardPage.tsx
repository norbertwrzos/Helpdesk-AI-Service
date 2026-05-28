export default function DashboardPage() {
  return (
    <div className="page">
      <div className="page__header">
        <h1 className="page__title">Dashboard</h1>
        <p className="page__subtitle">
          Przegląd systemu helpdesk — widok w przygotowaniu.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mt-6">
        {[
          { label: 'Otwarte zgłoszenia', value: '—', color: 'text-violet-400' },
          { label: 'Oczekujące', value: '—', color: 'text-yellow-400' },
          { label: 'Rozwiązane', value: '—', color: 'text-green-400' },
          { label: 'Odpowiedzi AI', value: '—', color: 'text-blue-400' },
        ].map((stat) => (
          <div
            key={stat.label}
            className="rounded-xl border border-gray-800 bg-gray-900/60 p-5"
          >
            <div className={`text-2xl font-bold ${stat.color}`}>{stat.value}</div>
            <div className="text-sm text-gray-500 mt-1">{stat.label}</div>
          </div>
        ))}
      </div>

      <div className="mt-8 rounded-xl border border-gray-800 bg-gray-900/60 p-6">
        <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3">
          Informacja
        </h2>
        <p className="text-gray-500 text-sm">
          Dashboard z metrykami i wykresami zostanie zaimplementowany w kolejnym etapie.
          Przejdź do <strong className="text-gray-300">Zgłoszeń</strong>, aby zarządzać ticketami.
        </p>
      </div>
    </div>
  )
}
