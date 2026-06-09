import { useNavigate } from 'react-router-dom'
import type { KnowledgeArticle } from '../types/knowledgeArticle'
import type { Category } from '../types/category'

interface Props {
  article: KnowledgeArticle
  categories: Category[]
  canEdit?: boolean
  onEdit?: (article: KnowledgeArticle) => void
  onDelete?: (id: number) => void
  /** Override the default /knowledge/:id navigation */
  onOpen?: () => void
}

function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString('pl-PL', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  })
}

export default function KnowledgeArticleCard({ article, categories, canEdit, onEdit, onDelete, onOpen }: Props) {
  const navigate = useNavigate()
  const category = categories.find(c => c.id === article.category_id)
  const showManagementActions = Boolean(canEdit && onEdit && onDelete)
  const tags = article.tags
    ? article.tags.split(',').map(t => t.trim()).filter(Boolean)
    : []
  const excerpt = article.content.length > 160
    ? article.content.slice(0, 160) + '…'
    : article.content

  return (
    <div className="surface-card surface-card--interactive flex h-full flex-col gap-4 p-5">
      {/* Category badge */}
      {category && (
        <span className="w-fit rounded-full border border-violet-800/40 bg-violet-900/30 px-2.5 py-1 text-xs font-medium text-violet-300">
          {category.name}
        </span>
      )}

      {/* Title */}
      <h3 className="line-clamp-2 text-base font-semibold leading-snug text-gray-100">
        {article.title}
      </h3>

      {/* Excerpt */}
      <p className="flex-1 line-clamp-3 text-sm leading-relaxed text-gray-400">
        {excerpt}
      </p>

      {/* Tags */}
      {tags.length > 0 && (
        <div className="flex flex-wrap gap-1.5">
          {tags.map(tag => (
            <span key={tag} className="rounded-full bg-white/5 px-2 py-1 text-xs text-gray-500">
              #{tag}
            </span>
          ))}
        </div>
      )}

      {/* Footer */}
      <div className="mt-auto flex items-center justify-between gap-3 border-t border-white/10 pt-3">
        <div className="flex items-center gap-2">
          {showManagementActions && (
            <>
              <button
                onClick={() => onEdit?.(article)}
                className="text-xs text-gray-400 transition-colors hover:text-violet-300"
              >
                Edytuj
              </button>
              <button
                onClick={() => onDelete?.(article.id)}
                className="text-xs text-gray-400 transition-colors hover:text-red-400"
              >
                Usuń
              </button>
            </>
          )}
          <button
            onClick={() => onOpen ? onOpen() : navigate(`/knowledge/${article.id}`)}
            className="rounded-full bg-white/5 px-3.5 py-1.5 text-xs font-semibold text-gray-200 transition-colors hover:bg-white/10"
          >
            Otwórz
          </button>
        </div>
      </div>
    </div>
  )
}
