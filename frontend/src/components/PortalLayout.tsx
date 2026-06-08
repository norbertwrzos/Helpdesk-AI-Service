import type { ReactNode } from 'react'

interface Props {
  children: ReactNode
}

export default function PortalLayout({ children }: Props) {
  return <div className="w-full">{children}</div>
}
