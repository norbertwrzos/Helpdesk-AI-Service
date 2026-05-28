interface Props {
  label: string
  value: number | string
  /** Tailwind text-color class for the value */
  valueColor?: string
  /** Optional small description below label */
  description?: string
}

/**
 * Single metric tile used on the Dashboard.
 */
export default function StatCard({ label, value, valueColor = 'text-violet-400', description }: Props) {
  return (
    <div className="rounded-xl border border-gray-800 bg-gray-900/60 p-5 flex flex-col gap-1">
      <div className={`text-3xl font-bold tabular-nums ${valueColor}`}>{value}</div>
      <div className="text-sm font-medium text-gray-300">{label}</div>
      {description && (
        <div className="text-xs text-gray-500 mt-1">{description}</div>
      )}
    </div>
  )
}
