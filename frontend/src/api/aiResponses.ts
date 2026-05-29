import { apiClient } from './client'
import type { AIResponse } from '../types/aiResponse'

export const getTicketAiResponses = (ticketId: number): Promise<AIResponse[]> =>
  apiClient.get(`/tickets/${ticketId}/ai-responses`)

export const getRecentAIResponses = (limit = 10): Promise<AIResponse[]> =>
  apiClient.get(`/ai-responses?limit=${limit}`)
