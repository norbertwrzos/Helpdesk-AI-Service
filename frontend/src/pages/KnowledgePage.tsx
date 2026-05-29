import { useEffect, useState } from 'react'
import { useAuth } from '../auth/AuthContext'
import { getArticles, createArticle, updateArticle, deleteArticle } from '../api/knowledge'
import { getCategories } from '../api/categories'
import type { KnowledgeArticle, KnowledgeArticleCreate, KnowledgeArticleUpdate } from '../types/knowledgeArticle'
import type { Category } from '../types/category'
import KnowledgeSearch from '../components/KnowledgeSearch'
import KnowledgeCategoryFilter from '../components/KnowledgeCategoryFilter'
import KnowledgeArticleCard from '../components/KnowledgeArticleCard'
import KnowledgeArticleForm from '../components/KnowledgeArticleForm'
import LoadingState from '../components/LoadingState'
import ErrorState from '../components/ErrorState'

export default function KnowledgePage() {
  const { role } = useAuth()
  const canEdit = role === 'admin' || role === 'agent'

  const [articles, setArticles] = useState<KnowledgeArticle[]>([])
  const [categories, setCategories] = useState<Category[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const [search, setSearch] = useState('')
  const [selectedCategory, setSelectedCategory] = useState<number | null>(null)

  const [formOpen, setFormOpen] = useState(false)
  const [editTarget, setEditTarget] = useState<KnowledgeArticle | null>(null)

  async function load() {
    setError(null)
    setLoading(true)
    try {
      const [arts, cats] = await Promise.all([getArticles(), getCategories()])
      setArticles(arts)
      setCategories(cats)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Błąd połączenia z serwerem.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  const filtered = articles.filter(a => {
    const q = search.toLowerCase()
    const matchSearch = !q || a.title.toLowerCase().includes(q) || a.content.toLowerCase().includes(q)
    const matchCat = selectedCategory === null || a.category_id === selectedCategory
    return matchSearch && matchCat
  })

  async function handleSubmit(data: KnowledgeArticleCreate | KnowledgeArticleUpdate) {
    if (editTarget) {
      await updateArticle(editTarget.id, data as KnowledgeArticleUpdate)
    } else {
      await createArticle(data as KnowledgeArticleCreate)
    }
    setFormOpen(false)
    setEditTarget(null)
    await load()
  }

  async function handleDelete(id: number) {
    if (!window.confirm('Czy na pewno chcesz usunąć ten artykuł?')) return
    try {
      await deleteArticle(id)
      await load()
    } catch (err) {
      alert(err instanceof Error ? err.message : 'Błąd usuwania.')
    }
  }

  function handleEdit(article: KnowledgeArticle) {
    setEditTarget(article)
    setFormOpen(true)
  }

  function handleAddNew() {
    setEditTarget(null)
    setFormOpen(true)
  }

  return (
    <div className="page space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between gap-4">
        <div>
          <h1 className="text-xl font-semibold text-gray-100">Baza wiedzy</h1>
          <p className="text-sm text-gray-500 mt-0.5">
            Artykuły i instrukcje wspierające obsługę najczęstszych problemów technicznych.
          </p>
        </div>
        {canEdit && (
          <button
            onClick={handleAddNew}
            className="flex items-center gap-2 bg-violet-600 hover:bg-violet-500 text-white text-sm font-medium px-4 py-2 rounded-lg transition-colors whitespace-nowrap"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2.5} className="w-4 h-4">
              <line x1="12" y1="5" x2="12" y2="19" />
              <line x1="5" y1="12" x2="19" y2="12" />
            </svg>
            Dodaj artykuł
          </button>
        )}
      </div>

      {/* Search */}
      <KnowledgeSearch value={search} onChange={setSearch} />

      {/* Category filter */}
      {categories.length > 0 && (
        <div className="space-y-2">
          <p className="text-xs font-semibold text-gray-600 uppercase tracking-wider">Kategorie</p>
          <KnowledgeCategoryFilter
            categories={categories}
            selected={selectedCategory}
            onChange={setSelectedCategory}
          />
        </div>
      )}

      {/* Content */}
      {loading ? (
        <LoadingState />
      ) : error ? (
        <ErrorState message={error} onRetry={load} />
      ) : filtered.length === 0 ? (
        <div className="text-center py-16 text-gray-600 text-sm">
          {search || selectedCategory ? 'Brak artykułów spełniających kryteria.' : 'Baza wiedzy jest pusta.'}
        </div>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
          {filtered.map(article => (
            <KnowledgeArticleCard
              key={article.id}
              article={article}
              categories={categories}
              canEdit={canEdit}
              onEdit={handleEdit}
              onDelete={handleDelete}
            />
          ))}
        </div>
      )}

      {formOpen && (
        <KnowledgeArticleForm
          article={editTarget}
          categories={categories}
          onSubmit={handleSubmit}
          onCancel={() => { setFormOpen(false); setEditTarget(null) }}
        />
      )}
    </div>
  )
}
