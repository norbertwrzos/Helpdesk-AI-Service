import { apiClient } from './client'
import type { Category, CategoryCreate } from '../types/category'

export const getCategories = (): Promise<Category[]> => apiClient.get('/categories')
export const createCategory = (data: CategoryCreate): Promise<Category> => apiClient.post('/categories', data)
