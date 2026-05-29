import type { Category } from '../types/category'

interface Props {
  categories: Category[]
  selected: number | null
  onChange: (id: number | null) => void
}

export default function KnowledgeCategoryFilter({ categories, selected, onChange }: Props) {
  return (
    <div className="flex flex-wrap gap-2">
      <button
        onClick={() => onChange(null)}
        className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
          selected === null
            ? 'bg-violet-600 text-white'
            : 'bg-gray-800 text-gray-400 hover:text-gray-200 hover:bg-gray-700'
        }`}
      >
        Wszystkie
      </button>
      {categories.map(cat => (
        <button
          key={cat.id}
          onClick={() => onChange(selected === cat.id ? null : cat.id)}
          className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
            selected === cat.id
              ? 'bg-violet-600 text-white'
              : 'bg-gray-800 text-gray-400 hover:text-gray-200 hover:bg-gray-700'
          }`}
        >
          {cat.name}
        </button>
      ))}
    </div>
  )
}
