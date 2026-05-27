import { apiClient } from './client'
import type { Category } from '../types/category'

export const getCategories = (): Promise<Category[]> => apiClient.get('/categories')
