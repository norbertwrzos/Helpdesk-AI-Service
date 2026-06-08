import { apiClient } from './client'
import type { Category, CategoryCreate, CategoryUpdate } from '../types/category'

export const getCategories = (): Promise<Category[]> => apiClient.get('/categories')
export const createCategory = (data: CategoryCreate): Promise<Category> => apiClient.post('/categories', data)
export const updateCategory = (categoryId: number, data: CategoryUpdate): Promise<Category> =>
	apiClient.patch(`/categories/${categoryId}`, data)
