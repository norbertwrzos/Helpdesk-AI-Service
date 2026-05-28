/**
 * Priority badge with colour coded by level.
 * level 1 = Niski (low), 2 = Średni (medium), 3 = Wysoki (high), 4+ = Krytyczny (critical)
 */
interface Props {
  name: string
  level: number
}

function colorByLevel(level: number): string {
  if (level >= 4) return 'bg-red-500/15 text-red-300 border-red-500/30'
  if (level === 3) return 'bg-orange-500/15 text-orange-300 border-orange-500/30'
  if (level === 2) return 'bg-blue-500/15 text-blue-300 border-blue-500/30'
  return 'bg-gray-700/60 text-gray-400 border-gray-600'
}

export default function PriorityBadge({ name, level }: Props) {
  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium border ${colorByLevel(level)}`}>
      {name}
    </span>
  )
}
