import { useState, useEffect } from 'react'
import type { KnowledgeArticle, KnowledgeArticleCreate, KnowledgeArticleUpdate } from '../types/knowledgeArticle'
import type { Category } from '../types/category'

interface Props {
  article?: KnowledgeArticle | null
  categories: Category[]
  onSubmit: (data: KnowledgeArticleCreate | KnowledgeArticleUpdate) => Promise<void>
  onCancel: () => void
}

export default function KnowledgeArticleForm({ article, categories, onSubmit, onCancel }: Props) {
  const [title, setTitle] = useState(article?.title ?? '')
  const [content, setContent] = useState(article?.content ?? '')
  const [categoryId, setCategoryId] = useState<string>(article?.category_id?.toString() ?? '')
  const [tags, setTags] = useState(article?.tags ?? '')
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    setTitle(article?.title ?? '')
    setContent(article?.content ?? '')
    setCategoryId(article?.category_id?.toString() ?? '')
    setTags(article?.tags ?? '')
  }, [article])

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!title.trim() || !content.trim()) {
      setError('Tytuł i treść są wymagane.')
      return
    }
    setSaving(true)
    setError(null)
    try {
      const payload: KnowledgeArticleCreate = {
        title: title.trim(),
        content: content.trim(),
        category_id: categoryId ? Number(categoryId) : null,
        tags: tags.trim() || null,
      }
      await onSubmit(payload)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Błąd zapisu.')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
      <div className="bg-gray-900 border border-gray-700 rounded-xl w-full max-w-2xl flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-800">
          <h2 className="text-gray-100 font-semibold">
            {article ? 'Edytuj artykuł' : 'Nowy artykuł'}
          </h2>
          <button
            onClick={onCancel}
            className="text-gray-500 hover:text-gray-300 transition-colors"
            aria-label="Zamknij"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-5 h-5">
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="flex flex-col gap-4 px-6 py-5 overflow-y-auto">
          {error && (
            <div className="bg-red-900/30 border border-red-800 text-red-300 text-sm px-4 py-2 rounded-lg">
              {error}
            </div>
          )}

          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-medium text-gray-400">Tytuł *</label>
            <input
              type="text"
              value={title}
              onChange={e => setTitle(e.target.value)}
              className="w-full px-3 py-2 rounded-lg bg-gray-800 border border-gray-700 text-gray-100 text-sm focus:outline-none focus:ring-2 focus:ring-violet-600 focus:border-transparent"
              placeholder="Tytuł artykułu"
            />
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-medium text-gray-400">Kategoria</label>
            <select
              value={categoryId}
              onChange={e => setCategoryId(e.target.value)}
              className="w-full px-3 py-2 rounded-lg bg-gray-800 border border-gray-700 text-gray-100 text-sm focus:outline-none focus:ring-2 focus:ring-violet-600 focus:border-transparent"
            >
              <option value="">— brak kategorii —</option>
              {categories.map(cat => (
                <option key={cat.id} value={cat.id}>{cat.name}</option>
              ))}
            </select>
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-medium text-gray-400">Tagi (oddzielone przecinkami)</label>
            <input
              type="text"
              value={tags}
              onChange={e => setTags(e.target.value)}
              className="w-full px-3 py-2 rounded-lg bg-gray-800 border border-gray-700 text-gray-100 text-sm focus:outline-none focus:ring-2 focus:ring-violet-600 focus:border-transparent"
              placeholder="np. vpn, hasło, sieć"
            />
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-medium text-gray-400">Treść *</label>
            <textarea
              value={content}
              onChange={e => setContent(e.target.value)}
              rows={10}
              className="w-full px-3 py-2 rounded-lg bg-gray-800 border border-gray-700 text-gray-100 text-sm focus:outline-none focus:ring-2 focus:ring-violet-600 focus:border-transparent resize-y font-mono"
              placeholder="Treść artykułu…"
            />
          </div>

          <div className="flex items-center justify-end gap-3 pt-2">
            <button
              type="button"
              onClick={onCancel}
              className="px-4 py-2 text-sm text-gray-400 hover:text-gray-200 transition-colors"
            >
              Anuluj
            </button>
            <button
              type="submit"
              disabled={saving}
              className="px-5 py-2 bg-violet-600 hover:bg-violet-500 disabled:opacity-50 text-white text-sm font-medium rounded-lg transition-colors"
            >
              {saving ? 'Zapisuję…' : article ? 'Zapisz zmiany' : 'Dodaj artykuł'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
