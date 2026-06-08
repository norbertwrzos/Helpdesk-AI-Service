import type { ReactNode } from 'react'
import { NavLink } from 'react-router-dom'

interface Props {
  to: string
  icon: ReactNode
  label: string
  end?: boolean
}

export default function NavItem({ to, icon, label, end = false }: Props) {
  return (
    <NavLink
      to={to}
      end={end}
      className={({ isActive }) =>
        `group flex w-full items-center gap-3 rounded-xl border px-3.5 py-3 text-sm font-medium transition-all duration-150 ${
          isActive
            ? 'border-white/10 bg-white/[0.07] text-white ring-1 ring-inset ring-white/5'
            : 'border-transparent text-slate-400 hover:border-white/5 hover:bg-white/[0.04] hover:text-slate-100'
        }`
      }
    >
      <span className="flex h-5 w-5 flex-shrink-0 items-center justify-center text-current">{icon}</span>
      <span className="truncate">{label}</span>
    </NavLink>
  )
}
