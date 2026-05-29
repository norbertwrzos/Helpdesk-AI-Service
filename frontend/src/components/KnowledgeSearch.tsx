interface Props {
  value: string
  onChange: (val: string) => void
}

export default function KnowledgeSearch({ value, onChange }: Props) {
  return (
    <div className="relative">
      <svg
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth={2}
        className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500 pointer-events-none"
      >
        <circle cx="11" cy="11" r="8" />
        <line x1="21" y1="21" x2="16.65" y2="16.65" />
      </svg>
      <input
        type="text"
        value={value}
        onChange={e => onChange(e.target.value)}
        placeholder="Szukaj artykułów po tytule lub treści…"
        className="w-full pl-12 pr-4 py-3.5 rounded-xl bg-gray-800 border border-gray-700 text-gray-100 placeholder-gray-500 text-sm focus:outline-none focus:ring-2 focus:ring-violet-600 focus:border-transparent transition-shadow"
      />
      {value && (
        <button
          onClick={() => onChange('')}
          className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-300 transition-colors"
          aria-label="Wyczyść"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-4 h-4">
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>
      )}
    </div>
  )
}
