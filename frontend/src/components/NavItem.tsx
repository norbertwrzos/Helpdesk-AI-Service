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
        `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors duration-150 w-full ${
          isActive
            ? 'bg-violet-600/20 text-violet-300 border border-violet-500/30'
            : 'text-gray-400 hover:bg-gray-800/60 hover:text-gray-200 border border-transparent'
        }`
      }
    >
      <span className="w-5 h-5 flex-shrink-0 flex items-center justify-center">{icon}</span>
      <span>{label}</span>
    </NavLink>
  )
}
