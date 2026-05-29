import { apiClient } from './client'
import type { Priority, PriorityCreate } from '../types/priority'

export const getPriorities = (): Promise<Priority[]> => apiClient.get('/priorities')
export const createPriority = (data: PriorityCreate): Promise<Priority> => apiClient.post('/priorities', data)
