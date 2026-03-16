import { Memory } from './types'

export interface KeywordStats {
  keyword: string
  count: number
  memories: Memory[]
  importance: number // 0-1
}

export function extractKeywords(memories: Memory[]): KeywordStats[] {
  const keywordMap = new Map<string, { count: number; memories: Memory[] }>()

  // 提取所有关键词
  memories.forEach(memory => {
    // 从标签中提取
    memory.tags.forEach(tag => {
      const key = tag.toLowerCase()
      if (!keywordMap.has(key)) {
        keywordMap.set(key, { count: 0, memories: [] })
      }
      const data = keywordMap.get(key)!
      data.count++
      if (!data.memories.find(m => m.id === memory.id)) {
        data.memories.push(memory)
      }
    })

    // 从内容中提取高频词
    const words = memory.content
      .toLowerCase()
      .split(/\s+|[，。！？；：""''（）【】《》、]/)
      .filter(w => w.length > 2 && !isCommonWord(w))

    words.forEach(word => {
      if (!keywordMap.has(word)) {
        keywordMap.set(word, { count: 0, memories: [] })
      }
      const data = keywordMap.get(word)!
      data.count++
      if (!data.memories.find(m => m.id === memory.id)) {
        data.memories.push(memory)
      }
    })
  })

  // 计算重要性并排序
  const maxCount = Math.max(...Array.from(keywordMap.values()).map(v => v.count))
  
  return Array.from(keywordMap.entries())
    .map(([keyword, data]) => ({
      keyword,
      count: data.count,
      memories: data.memories,
      importance: data.count / maxCount,
    }))
    .filter(k => k.count >= 2) // 只保留出现2次以上的关键词
    .sort((a, b) => b.count - a.count)
}

function isCommonWord(word: string): boolean {
  const commonWords = [
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
    'have', 'has', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
    'that', 'this', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
    '的', '了', '和', '是', '在', '有', '一', '个', '这', '那', '我', '你', '他',
    '她', '它', '们', '不', '很', '也', '都', '就', '还', '要', '可', '以', '为',
    '被', '把', '从', '到', '对', '给', '向', '让', '使', '叫', '比', '像', '如',
  ]
  return commonWords.includes(word)
}
