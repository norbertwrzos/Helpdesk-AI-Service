import RoleBasedNavigation from './RoleBasedNavigation'

export default function Sidebar() {
  return (
    <aside className="fixed left-0 top-0 h-screen w-64 bg-sidebar border-r border-gray-800 flex flex-col z-20">
      {/* Brand */}
      <div className="flex items-center gap-3 px-5 h-16 border-b border-gray-800 flex-shrink-0">
        <div className="w-8 h-8 bg-violet-600 rounded-lg flex items-center justify-center text-sm font-bold text-white">
          H
        </div>
        <div>
          <div className="text-sm font-semibold text-gray-100 leading-none">Helpdesk AI</div>
          <div className="text-xs text-gray-500 mt-0.5">Service</div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 py-4 px-3 overflow-y-auto">
        <RoleBasedNavigation />
      </nav>

      {/* Footer */}
      <div className="px-4 py-3 border-t border-gray-800 flex-shrink-0">
        <div className="text-xs text-gray-700">Prototyp · praca inżynierska</div>
      </div>
    </aside>
  )
}
