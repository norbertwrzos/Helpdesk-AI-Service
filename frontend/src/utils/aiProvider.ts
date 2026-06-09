export interface ProviderDisplay {
  label: string
  badgeClassName: string
}

export function getProviderDisplay(providerName: string | null | undefined): ProviderDisplay {
  const normalized = providerName?.trim().toLowerCase()

  if (normalized === 'openai') {
    return {
      label: 'OpenAI RAG',
      badgeClassName: 'bg-violet-500/15 text-violet-300 border border-violet-500/30',
    }
  }

  if (normalized === 'mock') {
    return {
      label: 'Tryb testowy',
      badgeClassName: 'bg-slate-500/15 text-slate-300 border border-slate-500/30',
    }
  }

  return {
    label: 'Nieznany provider',
    badgeClassName: 'bg-gray-500/15 text-gray-300 border border-gray-500/30',
  }
}