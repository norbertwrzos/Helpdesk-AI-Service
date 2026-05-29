type TabKey = 'categories' | 'priorities' | 'profile' | 'email'

const TABS: { key: TabKey; label: string }[] = [
  { key: 'categories', label: 'Kategorie' },
  { key: 'priorities', label: 'Priorytety' },
  { key: 'profile',    label: 'Profil' },
  { key: 'email',      label: 'E-mail supportu' },
]

interface Props {
  active: TabKey
  onChange: (tab: TabKey) => void
}

export default function SettingsTabs({ active, onChange }: Props) {
  return (
    <div className="flex gap-1 border-b border-gray-800 mb-6">
      {TABS.map(tab => (
        <button
          key={tab.key}
          onClick={() => onChange(tab.key)}
          className={[
            'px-4 py-2 text-sm font-medium rounded-t-lg transition-colors',
            active === tab.key
              ? 'text-cyan-300 border-b-2 border-cyan-400 -mb-px'
              : 'text-gray-500 hover:text-gray-300',
          ].join(' ')}
        >
          {tab.label}
        </button>
      ))}
    </div>
  )
}

export type { TabKey }
