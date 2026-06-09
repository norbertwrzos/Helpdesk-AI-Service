/**
 * Centralised date formatting helpers (pl-PL locale).
 *
 * Extracted during the pre-demo review (Etap 12.5) to remove identical
 * `formatDate` helpers that were duplicated across several components.
 */

/** Format an ISO timestamp as a medium date with a short time, e.g. "9 cze 2026, 14:30". */
export function formatDateTime(iso: string): string {
  return new Date(iso).toLocaleString('pl-PL', { dateStyle: 'medium', timeStyle: 'short' })
}
