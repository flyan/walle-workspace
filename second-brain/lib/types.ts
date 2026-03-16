export interface Memory {
  id: string
  title: string
  content: string
  type: 'memory' | 'conversation' | 'note'
  agent: 'main' | 'coder' | 'writer'
  date: string
  tags: string[]
  path: string
}

export interface FilterOptions {
  type?: string
  agent?: string
  dateFrom?: string
  dateTo?: string
  searchQuery?: string
}
