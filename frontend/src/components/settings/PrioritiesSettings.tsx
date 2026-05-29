import { useEffect, useState } from 'react'
import { getPriorities, createPriority } from '../../api/priorities'
import type { Priority } from '../../types/priority'
import { useToast } from '../../context/ToastContext'

interface Props {
  isAdmin: boolean
}

const LEVEL_COLORS: Record<number, { dot: string; badge: string }> = {
  1: { dot: 'bg-gray-400',   badge: 'text-gray-400 border-gray-700' },
  2: { dot: 'bg-blue-400',   badge: 'text-blue-400 border-blue-700' },
  3: { dot: 'bg-orange-400', badge: 'text-orange-400 border-orange-700' },
  4: { dot: 'bg-red-500',    badge: 'text-red-400 border-red-700' },
}

function getLevelColors(level: number) {
  return LEVEL_COLORS[level] ?? LEVEL_COLORS[1]
}

export default function PrioritiesSettings({ isAdmin }: Props) {
  const { showToast } = useToast()
  const [priorities, setPriorities] = useState<Priority[]>([])
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [name, setName] = useState('')
  const [level, setLevel] = useState(1)
  const [description, setDescription] = useState('')

  async function load() {
    setLoading(true)
    try {
      const data = await getPriorities()
      setPriorities(data.sort((a, b) => a.level - b.level))
    } catch {
      showToast('Nie udało się załadować priorytetów.', 'error')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  async function handleAdd(e: React.FormEvent) {
    e.preventDefault()
    if (!name.trim()) return
    setSaving(true)
    try {
      const created = await createPriority({ name: name.trim(), level, description: description.trim() || null })
      setPriorities(prev => [...prev, created].sort((a, b) => a.level - b.level))
      setName('')
      setLevel(1)
      setDescription('')
      showToast('Priorytet dodany.', 'success')
    } catch {
      showToast('Nie udało się dodać priorytetu.', 'error')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="rounded-xl border border-gray-800 bg-gray-900/60 overflow-hidden">
        <div className="px-5 py-3 border-b border-gray-800">
          <h3 className="text-sm font-semibold text-gray-200">Lista priorytetów</h3>
        </div>
        {loading ? (
          <div className="px-5 py-6 text-sm text-gray-500">Ładowanie…</div>
        ) : priorities.length === 0 ? (
          <div className="px-5 py-6 text-sm text-gray-500">Brak priorytetów.</div>
        ) : (
          <ul className="divide-y divide-gray-800">
            {priorities.map(p => {
              const colors = getLevelColors(p.level)
              return (
                <li key={p.id} className="px-5 py-3 flex items-center justify-between gap-4">
                  <div className="flex items-center gap-3">
                    <span className={`w-2.5 h-2.5 rounded-full shrink-0 ${colors.dot}`} />
                    <div>
                      <div className="text-sm font-medium text-gray-200">{p.name}</div>
                      {p.description && (
                        <div className="text-xs text-gray-500 mt-0.5">{p.description}</div>
                      )}
                    </div>
                  </div>
                  <span className={`text-xs border rounded-full px-2 py-0.5 ${colors.badge}`}>
                    poziom {p.level}
                  </span>
                </li>
              )
            })}
          </ul>
        )}
      </div>

      {isAdmin && (
        <div className="rounded-xl border border-gray-800 bg-gray-900/60 p-5">
          <h3 className="text-sm font-semibold text-gray-200 mb-4">Dodaj priorytet</h3>
          <form onSubmit={handleAdd} className="space-y-3">
            <div>
              <label className="block text-xs text-gray-400 mb-1">Nazwa *</label>
              <input
                type="text"
                value={name}
                onChange={e => setName(e.target.value)}
                required
                placeholder="np. Niski, Krytyczny…"
                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm text-gray-200 placeholder-gray-600 focus:outline-none focus:border-cyan-500/60"
              />
            </div>
            <div>
              <label className="block text-xs text-gray-400 mb-1">Poziom *</label>
              <select
                value={level}
                onChange={e => setLevel(Number(e.target.value))}
                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm text-gray-200 focus:outline-none focus:border-cyan-500/60"
              >
                <option value={1}>1 — Niski</option>
                <option value={2}>2 — Średni</option>
                <option value={3}>3 — Wysoki</option>
                <option value={4}>4 — Krytyczny</option>
              </select>
            </div>
            <div>
              <label className="block text-xs text-gray-400 mb-1">Opis</label>
              <input
                type="text"
                value={description}
                onChange={e => setDescription(e.target.value)}
                placeholder="Opcjonalny opis"
                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm text-gray-200 placeholder-gray-600 focus:outline-none focus:border-cyan-500/60"
              />
            </div>
            <button
              type="submit"
              disabled={saving || !name.trim()}
              className="px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 disabled:opacity-50 text-sm font-medium text-white transition-colors"
            >
              {saving ? 'Zapisywanie…' : 'Dodaj priorytet'}
            </button>
          </form>
        </div>
      )}
    </div>
  )
}
