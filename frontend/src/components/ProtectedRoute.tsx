import { Navigate } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'
import type { UserRole } from '../types/auth'

interface Props {
  children: React.ReactNode
  allowedRoles?: UserRole[]
  /** redirect destination when role doesn't match; defaults to '/' */
  redirectTo?: string
}

/**
 * Wraps a route so that only authenticated users with an allowed role can see it.
 * - Not logged in  → /login
 * - Wrong role     → redirectTo (default: '/')
 */
export default function ProtectedRoute({ children, allowedRoles, redirectTo = '/' }: Props) {
  const { currentUser } = useAuth()

  if (!currentUser) {
    return <Navigate to="/login" replace />
  }

  if (allowedRoles && !allowedRoles.includes(currentUser.role)) {
    return <Navigate to={redirectTo} replace />
  }

  return <>{children}</>
}
