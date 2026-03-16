'use client'

import { useState, useEffect } from 'react'
import { Memory } from '@/lib/types'
import { KeywordStats, extractKeywords } from '@/lib/keywords'
import KeywordCloud from '@/app/components/KeywordCloud'
import MemoryList from '@/app/components/MemoryList'

export default function KeywordsPage() {
  const [memories, setMemories] = useState<Memory[]>([])
  const [keywords, setKeywords] = useState<KeywordStats[]>([])
  const [selectedKeyword, setSelectedKeyword] = useState<string>('')
  const [selectedMemory, setSelectedMemory] = useState<Memory | null>(null)
  const [loading, setLoading] = useState(true)

  // 加载记忆
  useEffect(() => {
    const loadMemories = async () => {
      try {
        const response = await fetch('/api/memories')
        const data = await response.json()
        setMemories(data)
        
        // 提取关键词
        const kws = extractKeywords(data)
        setKeywords(kws)
      } catch (error) {
        console.error('Failed to load memories:', error)
      } finally {
        setLoading(false)
      }
    }

    loadMemories()
  }, [])

  // 获取选中关键词的相关记忆
  const relatedMemories = selectedKeyword
    ? keywords.find(k => k.keyword === selectedKeyword)?.memories || []
    : []

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-slate-400">加载中...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-slate-950">
      <div className="max-w-7xl mx-auto">
        {/* 头部 */}
        <header className="border-b border-slate-800 py-6 px-4">
          <h1 className="text-3xl font-bold text-slate-100 mb-2">关键词云</h1>
          <p className="text-slate-400">点击关键词查看相关内容</p>
        </header>

        {/* 关键词云 */}
        <div className="p-6 border-b border-slate-800">
          <KeywordCloud
            keywords={keywords}
            selectedKeyword={selectedKeyword}
            onSelect={setSelectedKeyword}
          />
        </div>

        {/* 相关内容 */}
        {selectedKeyword && (
          <div className="p-6">
            <div className="mb-4">
              <h2 className="text-xl font-semibold text-slate-100">
                关键词：<span className="text-blue-400">{selectedKeyword}</span>
              </h2>
              <p className="text-sm text-slate-400 mt-1">
                找到 {relatedMemories.length} 条相关内容
              </p>
            </div>

            <MemoryList
              memories={relatedMemories}
              selectedId={selectedMemory?.id}
              onSelect={setSelectedMemory}
            />
          </div>
        )}

        {!selectedKeyword && (
          <div className="p-6 text-center text-slate-400">
            点击上方关键词查看相关内容
          </div>
        )}
      </div>
    </div>
  )
}
