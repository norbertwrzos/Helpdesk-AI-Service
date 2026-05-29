import { useNavigate } from 'react-router-dom'
import type { KnowledgeArticle } from '../types/knowledgeArticle'
import type { Category } from '../types/category'

interface Props {
  article: KnowledgeArticle
  categories: Category[]
  canEdit: boolean
  onEdit: (article: KnowledgeArticle) => void
  onDelete: (id: number) => void
}

function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString('pl-PL', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  })
}

export default function KnowledgeArticleCard({ article, categories, canEdit, onEdit, onDelete }: Props) {
  const navigate = useNavigate()
  const category = categories.find(c => c.id === article.category_id)
  const tags = article.tags
    ? article.tags.split(',').map(t => t.trim()).filter(Boolean)
    : []
  const excerpt = article.content.length > 160
    ? article.content.slice(0, 160) + '…'
    : article.content

  return (
    <div className="bg-gray-900 border border-gray-800 rounded-xl p-5 flex flex-col gap-3 hover:border-gray-700 transition-colors">
      {/* Category badge */}
      {category && (
        <span className="text-xs font-medium text-violet-400 bg-violet-900/30 border border-violet-800/40 px-2 py-0.5 rounded-full w-fit">
          {category.name}
        </span>
      )}

      {/* Title */}
      <h3 className="text-gray-100 font-semibold text-sm leading-snug line-clamp-2">
        {article.title}
      </h3>

      {/* Excerpt */}
      <p className="text-gray-500 text-xs leading-relaxed line-clamp-3 flex-1">
        {excerpt}
      </p>

      {/* Tags */}
      {tags.length > 0 && (
        <div className="flex flex-wrap gap-1">
          {tags.map(tag => (
            <span key={tag} className="text-xs text-gray-600 bg-gray-800 px-2 py-0.5 rounded">
              #{tag}
            </span>
          ))}
        </div>
      )}

      {/* Footer */}
      <div className="flex items-center justify-between pt-1 border-t border-gray-800">
        <span className="text-xs text-gray-600">
          Aktualizacja: {formatDate(article.updated_at)}
        </span>
        <div className="flex items-center gap-2">
          {canEdit && (
            <>
              <button
                onClick={() => onEdit(article)}
                className="text-xs text-gray-500 hover:text-violet-400 transition-colors"
              >
                Edytuj
              </button>
              <button
                onClick={() => onDelete(article.id)}
                className="text-xs text-gray-500 hover:text-red-400 transition-colors"
              >
                Usuń
              </button>
            </>
          )}
          <button
            onClick={() => navigate(`/knowledge/${article.id}`)}
            className="text-xs font-medium bg-gray-800 hover:bg-gray-700 text-gray-300 px-3 py-1.5 rounded-lg transition-colors"
          >
            Otwórz
          </button>
        </div>
      </div>
    </div>
  )
}
