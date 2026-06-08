import { apiClient } from './client'
import type { Priority, PriorityCreate, PriorityUpdate } from '../types/priority'

export const getPriorities = (): Promise<Priority[]> => apiClient.get('/priorities')
export const createPriority = (data: PriorityCreate): Promise<Priority> => apiClient.post('/priorities', data)
export const updatePriority = (priorityId: number, data: PriorityUpdate): Promise<Priority> =>
	apiClient.patch(`/priorities/${priorityId}`, data)
