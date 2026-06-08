import { useEffect, useState } from 'react'
import { createCategory, getCategories, updateCategory } from '../../api/categories'
import type { Category } from '../../types/category'
import { useToast } from '../../context/ToastContext'

interface Props {
  canManage: boolean
}

export default function CategoriesSettings({ canManage }: Props) {
  const { showToast } = useToast()
  const [categories, setCategories] = useState<Category[]>([])
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [updatingId, setUpdatingId] = useState<number | null>(null)
  const [editingId, setEditingId] = useState<number | null>(null)
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [editName, setEditName] = useState('')
  const [editDescription, setEditDescription] = useState('')

  async function load() {
    setLoading(true)
    try {
      const data = await getCategories()
      setCategories(data)
    } catch {
      showToast('Nie udało się załadować kategorii.', 'error')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  function startEditing(category: Category) {
    setEditingId(category.id)
    setEditName(category.name)
    setEditDescription(category.description ?? '')
  }

  function stopEditing() {
    setEditingId(null)
    setEditName('')
    setEditDescription('')
  }

  async function handleAdd(e: React.FormEvent) {
    e.preventDefault()
    if (!name.trim()) return
    setSaving(true)
    try {
      const created = await createCategory({ name: name.trim(), description: description.trim() || null })
      setCategories(prev => [...prev, created])
      setName('')
      setDescription('')
      showToast('Kategoria dodana.', 'success')
    } catch {
      showToast('Nie udało się dodać kategorii.', 'error')
    } finally {
      setSaving(false)
    }
  }

  async function handleUpdate(e: React.FormEvent, categoryId: number) {
    e.preventDefault()
    if (!editName.trim()) return

    setUpdatingId(categoryId)
    try {
      const updated = await updateCategory(categoryId, {
        name: editName.trim(),
        description: editDescription.trim() || null,
      })
      setCategories((prev) => prev.map((category) => (
        category.id === categoryId ? updated : category
      )))
      stopEditing()
      showToast('Kategoria zaktualizowana.', 'success')
    } catch {
      showToast('Nie udało się zapisać kategorii.', 'error')
    } finally {
      setUpdatingId(null)
    }
  }

  return (
    <div className="space-y-6">
      <div className="rounded-xl border border-gray-800 bg-gray-900/60 overflow-hidden">
        <div className="px-5 py-3 border-b border-gray-800">
          <h3 className="text-sm font-semibold text-gray-200">Lista kategorii</h3>
        </div>
        {loading ? (
          <div className="px-5 py-6 text-sm text-gray-500">Ładowanie…</div>
        ) : categories.length === 0 ? (
          <div className="px-5 py-6 text-sm text-gray-500">Brak kategorii.</div>
        ) : (
          <ul className="divide-y divide-gray-800">
            {categories.map(cat => (
              <li key={cat.id} className="px-5 py-3">
                {editingId === cat.id ? (
                  <form onSubmit={(e) => void handleUpdate(e, cat.id)} className="space-y-3">
                    <div>
                      <label className="block text-xs text-gray-400 mb-1">Nazwa *</label>
                      <input
                        type="text"
                        value={editName}
                        onChange={e => setEditName(e.target.value)}
                        required
                        className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm text-gray-200 placeholder-gray-600 focus:outline-none focus:border-cyan-500/60"
                      />
                    </div>
                    <div>
                      <label className="block text-xs text-gray-400 mb-1">Opis</label>
                      <input
                        type="text"
                        value={editDescription}
                        onChange={e => setEditDescription(e.target.value)}
                        className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm text-gray-200 placeholder-gray-600 focus:outline-none focus:border-cyan-500/60"
                      />
                    </div>
                    <div className="flex items-center justify-between gap-3">
                      <span className="text-xs text-gray-700">#{cat.id}</span>
                      <div className="flex items-center gap-2">
                        <button
                          type="button"
                          onClick={stopEditing}
                          disabled={updatingId === cat.id}
                          className="px-3 py-2 rounded-lg border border-gray-700 text-sm text-gray-300 transition-colors hover:border-gray-600 hover:text-gray-100 disabled:opacity-50"
                        >
                          Anuluj
                        </button>
                        <button
                          type="submit"
                          disabled={updatingId === cat.id || !editName.trim()}
                          className="px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 disabled:opacity-50 text-sm font-medium text-white transition-colors"
                        >
                          {updatingId === cat.id ? 'Zapisywanie…' : 'Zapisz'}
                        </button>
                      </div>
                    </div>
                  </form>
                ) : (
                  <div className="flex items-start justify-between gap-4">
                    <div>
                      <div className="text-sm font-medium text-gray-200">{cat.name}</div>
                      {cat.description && (
                        <div className="text-xs text-gray-500 mt-0.5">{cat.description}</div>
                      )}
                    </div>
                    <div className="flex items-center gap-3">
                      {canManage && (
                        <button
                          type="button"
                          onClick={() => startEditing(cat)}
                          className="px-3 py-1.5 rounded-lg border border-gray-700 text-xs font-medium text-gray-300 transition-colors hover:border-cyan-500/40 hover:text-cyan-300"
                        >
                          Edytuj
                        </button>
                      )}
                      <span className="text-xs text-gray-700 mt-0.5">#{cat.id}</span>
                    </div>
                  </div>
                )}
              </li>
            ))}
          </ul>
        )}
      </div>

      {canManage && (
        <div className="rounded-xl border border-gray-800 bg-gray-900/60 p-5">
          <h3 className="text-sm font-semibold text-gray-200 mb-4">Dodaj kategorię</h3>
          <form onSubmit={handleAdd} className="space-y-3">
            <div>
              <label className="block text-xs text-gray-400 mb-1">Nazwa *</label>
              <input
                type="text"
                value={name}
                onChange={e => setName(e.target.value)}
                required
                placeholder="np. Sieć, Hardware…"
                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm text-gray-200 placeholder-gray-600 focus:outline-none focus:border-cyan-500/60"
              />
            </div>
            <div>
              <label className="block text-xs text-gray-400 mb-1">Opis</label>
              <input
                type="text"
                value={description}
                onChange={e => setDescription(e.target.value)}
                placeholder="Opcjonalny opis kategorii"
                className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm text-gray-200 placeholder-gray-600 focus:outline-none focus:border-cyan-500/60"
              />
            </div>
            <button
              type="submit"
              disabled={saving || !name.trim()}
              className="px-4 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 disabled:opacity-50 text-sm font-medium text-white transition-colors"
            >
              {saving ? 'Zapisywanie…' : 'Dodaj kategorię'}
            </button>
          </form>
        </div>
      )}
    </div>
  )
}
