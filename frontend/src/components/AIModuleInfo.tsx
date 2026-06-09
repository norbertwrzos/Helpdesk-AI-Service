const items = [
  {
    label: 'Tryb działania',
    value: 'Mock / rule-based',
    note: 'Brak połączenia z zewnętrznym LLM. Odpowiedzi generowane na podstawie reguł.',
  },
  {
    label: 'Uruchamianie analizy',
    value: 'Widok szczegółów zgłoszenia',
    note: 'Analiza dostępna po otwarciu konkretnego zgłoszenia → przycisk „Analizuj".',
  },
  {
    label: 'Weryfikacja odpowiedzi',
    value: 'Wymagana przez agenta',
    note: 'Każda odpowiedź AI powinna zostać sprawdzona przez agenta przed wysłaniem.',
  },
]

export default function AIModuleInfo() {
  return (
    <div className="rounded-xl border border-gray-800 bg-gray-900/60 divide-y divide-gray-800">
      {items.map((item) => (
        <div key={item.label} className="flex items-start gap-4 px-5 py-4">
          <div className="flex-1 min-w-0">
            <div className="flex flex-wrap items-baseline gap-2">
              <span className="text-xs font-semibold uppercase tracking-wider text-gray-500">
                {item.label}
              </span>
              <span className="text-sm font-medium text-violet-300">{item.value}</span>
            </div>
            <p className="mt-0.5 text-xs text-gray-500">{item.note}</p>
          </div>
        </div>
      ))}
    </div>
  )
}
