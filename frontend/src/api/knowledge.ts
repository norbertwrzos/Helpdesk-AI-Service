import { apiClient } from './client'
import type { KnowledgeArticle, KnowledgeArticleCreate, KnowledgeArticleUpdate } from '../types/knowledgeArticle'

export const getArticles = (): Promise<KnowledgeArticle[]> =>
  apiClient.get('/knowledge')

export const getArticle = (id: number): Promise<KnowledgeArticle> =>
  apiClient.get(`/knowledge/${id}`)

export const createArticle = (payload: KnowledgeArticleCreate): Promise<KnowledgeArticle> =>
  apiClient.post('/knowledge', payload)

export const updateArticle = (id: number, payload: KnowledgeArticleUpdate): Promise<KnowledgeArticle> =>
  apiClient.patch(`/knowledge/${id}`, payload)

export const deleteArticle = async (id: number): Promise<void> => {
  const BASE_URL = (import.meta.env.VITE_API_BASE_URL as string) || 'http://localhost:8000'
  const response = await fetch(`${BASE_URL}/knowledge/${id}`, { method: 'DELETE' })
  if (!response.ok && response.status !== 204) {
    throw new Error(`HTTP ${response.status}`)
  }
}
