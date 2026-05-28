export default function KnowledgePage() {
  return (
    <div className="page">
      <div className="page__header">
        <h1 className="page__title">Baza wiedzy</h1>
        <p className="page__subtitle">
          Artykuły i rozwiązania problemów technicznych — widok w przygotowaniu.
        </p>
      </div>

      <div className="mt-6 rounded-xl border border-gray-800 bg-gray-900/60 p-6">
        <p className="text-gray-500 text-sm">
          Przeglądarka artykułów bazy wiedzy zostanie zaimplementowana w kolejnym etapie.
          Artykuły są dostępne przez API (<code className="text-violet-400">/knowledge</code>).
        </p>
      </div>
    </div>
  )
}
