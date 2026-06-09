import type { ParsedSources, RagSource } from '../types/aiResponse'

function asNumber(value: unknown): number | null {
  if (typeof value === 'number' && Number.isFinite(value)) {
    return value
  }

  if (typeof value === 'string' && value.trim() !== '') {
    const parsed = Number(value)
    return Number.isFinite(parsed) ? parsed : null
  }

  return null
}

function asString(value: unknown): string | null {
  return typeof value === 'string' && value.trim() !== '' ? value.trim() : null
}

function normalizeSource(item: unknown): RagSource | null {
  if (!item || typeof item !== 'object') {
    return null
  }

  const record = item as Record<string, unknown>
  const articleId = asNumber(record.article_id ?? record.id)
  const title = asString(record.title) ?? (articleId !== null ? `Artykuł #${articleId}` : 'Źródło RAG')

  return {
    article_id: articleId,
    title,
    score: asNumber(record.score),
    excerpt: asString(record.excerpt),
    used_by_model: typeof record.used_by_model === 'boolean' ? record.used_by_model : null,
    source_type: asString(record.source_type),
  }
}

function normalizeSourcesArray(items: unknown[]): RagSource[] {
  return items
    .map(normalizeSource)
    .filter((source): source is RagSource => source !== null)
}

export function parseSourcesUsed(sourcesUsed: string | null | undefined): ParsedSources {
  if (!sourcesUsed || sourcesUsed.trim() === '') {
    return { sources: [] }
  }

  try {
    const parsed = JSON.parse(sourcesUsed) as unknown

    if (Array.isArray(parsed)) {
      return { sources: normalizeSourcesArray(parsed) }
    }

    if (parsed && typeof parsed === 'object') {
      const record = parsed as Record<string, unknown>

      if (Array.isArray(record.sources)) {
        return { sources: normalizeSourcesArray(record.sources) }
      }

      const singleSource = normalizeSource(record)
      if (singleSource) {
        return { sources: [singleSource] }
      }
    }
  } catch {
    return {
      sources: [],
      parse_error: 'Nie udało się odczytać metadanych źródeł.',
    }
  }

  return {
    sources: [],
    parse_error: 'Nie udało się odczytać metadanych źródeł.',
  }
}