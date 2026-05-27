import { apiClient } from './client'
import type { Priority } from '../types/priority'

export const getPriorities = (): Promise<Priority[]> => apiClient.get('/priorities')
