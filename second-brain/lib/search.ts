import { Memory, FilterOptions } from './types'

export function searchMemories(memories: Memory[], options: FilterOptions): Memory[] {
  return memories.filter(memory => {
    // 搜索查询
    if (options.searchQuery) {
      const query = options.searchQuery.toLowerCase()
      const matchesTitle = memory.title.toLowerCase().includes(query)
      const matchesContent = memory.content.toLowerCase().includes(query)
      const matchesTags = memory.tags.some(tag => tag.toLowerCase().includes(query))
      
      if (!matchesTitle && !matchesContent && !matchesTags) {
        return false
      }
    }

    // 类型筛选
    if (options.type && memory.type !== options.type) {
      return false
    }

    // Agent 筛选
    if (options.agent && memory.agent !== options.agent) {
      return false
    }

    // 日期范围筛选
    if (options.dateFrom && memory.date < options.dateFrom) {
      return false
    }
    if (options.dateTo && memory.date > options.dateTo) {
      return false
    }

    return true
  })
}

export function highlightSearchResults(text: string, query: string): string {
  if (!query) return text
  
  const regex = new RegExp(`(${query})`, 'gi')
  return text.replace(regex, '<mark>$1</mark>')
}
