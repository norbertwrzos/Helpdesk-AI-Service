export interface KnowledgeArticle {
  id: number
  title: string
  content: string
  category_id: number | null
  tags: string | null
  created_at: string
  updated_at: string
}

export interface KnowledgeArticleCreate {
  title: string
  content: string
  category_id?: number | null
  tags?: string | null
}

export interface KnowledgeArticleUpdate {
  title?: string
  content?: string
  category_id?: number | null
  tags?: string | null
}
