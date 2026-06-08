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

export const deleteArticle = (id: number): Promise<void> =>
  apiClient.delete(`/knowledge/${id}`)
