import { createContext, useContext, useState, useEffect, type ReactNode } from 'react'
import type { MockUser, UserRole } from '../types/auth'
import { MOCK_USERS } from './mockUsers'

const STORAGE_KEY = 'helpdesk_mock_user'

interface AuthContextValue {
  currentUser: MockUser | null
  role: UserRole | null
  login: (userId: string) => void
  logout: () => void
}

const AuthContext = createContext<AuthContextValue | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [currentUser, setCurrentUser] = useState<MockUser | null>(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY)
      if (!stored) return null
      const user = MOCK_USERS.find(u => u.id === stored)
      return user ?? null
    } catch {
      return null
    }
  })

  useEffect(() => {
    if (currentUser) {
      localStorage.setItem(STORAGE_KEY, currentUser.id)
    } else {
      localStorage.removeItem(STORAGE_KEY)
    }
  }, [currentUser])

  function login(userId: string) {
    const user = MOCK_USERS.find(u => u.id === userId)
    if (user) setCurrentUser(user)
  }

  function logout() {
    setCurrentUser(null)
  }

  return (
    <AuthContext.Provider value={{ currentUser, role: currentUser?.role ?? null, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
