import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getArticle } from '../api/knowledge'
import { getCategories } from '../api/categories'
import type { KnowledgeArticle } from '../types/knowledgeArticle'
import type { Category } from '../types/category'
import LoadingState from '../components/LoadingState'
import ErrorState from '../components/ErrorState'

function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString('pl-PL', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

export default function KnowledgeArticlePage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()

  const [article, setArticle] = useState<KnowledgeArticle | null>(null)
  const [categories, setCategories] = useState<Category[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  async function load() {
    if (!id) return
    setError(null)
    setLoading(true)
    try {
      const [art, cats] = await Promise.all([getArticle(Number(id)), getCategories()])
      setArticle(art)
      setCategories(cats)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Nie udało się załadować artykułu.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [id])

  const category = article ? categories.find(c => c.id === article.category_id) : null
  const tags = article?.tags
    ? article.tags.split(',').map(t => t.trim()).filter(Boolean)
    : []

  return (
    <div className="page max-w-3xl mx-auto space-y-6">
      {/* Back button */}
      <button
        onClick={() => navigate('/knowledge')}
        className="flex items-center gap-2 text-sm text-gray-500 hover:text-violet-400 transition-colors group"
      >
        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth={2}
          className="w-4 h-4 group-hover:-translate-x-0.5 transition-transform"
        >
          <line x1="19" y1="12" x2="5" y2="12" />
          <polyline points="12 19 5 12 12 5" />
        </svg>
        Wróć do bazy wiedzy
      </button>

      {loading ? (
        <LoadingState />
      ) : error ? (
        <ErrorState message={error} onRetry={load} />
      ) : article ? (
        <article className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
          {/* Article header */}
          <div className="px-6 py-5 border-b border-gray-800 space-y-3">
            {category && (
              <span className="text-xs font-medium text-violet-400 bg-violet-900/30 border border-violet-800/40 px-2.5 py-0.5 rounded-full">
                {category.name}
              </span>
            )}
            <h1 className="text-xl font-semibold text-gray-100 leading-snug">
              {article.title}
            </h1>
            {tags.length > 0 && (
              <div className="flex flex-wrap gap-1.5">
                {tags.map(tag => (
                  <span key={tag} className="text-xs text-gray-500 bg-gray-800 px-2 py-0.5 rounded">
                    #{tag}
                  </span>
                ))}
              </div>
            )}
            <div className="flex gap-4 text-xs text-gray-600">
              <span>Utworzono: {formatDate(article.created_at)}</span>
              <span>Aktualizacja: {formatDate(article.updated_at)}</span>
            </div>
          </div>

          {/* Article content */}
          <div className="px-6 py-5">
            <pre className="whitespace-pre-wrap font-sans text-sm text-gray-300 leading-relaxed">
              {article.content}
            </pre>
          </div>
        </article>
      ) : null}
    </div>
  )
}
