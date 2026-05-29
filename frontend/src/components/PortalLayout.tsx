import type { ReactNode } from 'react'

interface Props {
  children: ReactNode
}

/**
 * PortalLayout — thin wrapper for end-user portal pages.
 * Currently just passes children through; can be extended with
 * portal-specific chrome (breadcrumbs, welcome banner, etc.).
 */
export default function PortalLayout({ children }: Props) {
  return <>{children}</>
}
