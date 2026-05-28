export type UserRole = 'admin' | 'agent' | 'end_user'

export interface MockUser {
  id: string
  email: string
  name: string
  role: UserRole
}
