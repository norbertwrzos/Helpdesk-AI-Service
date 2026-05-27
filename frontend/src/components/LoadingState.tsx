export default function LoadingState({ label = 'Ładowanie…' }: { label?: string }) {
  return (
    <div className="loading-state">
      <span className="loading-state__spinner" />
      <span>{label}</span>
    </div>
  )
}
