'use client'

import { useState, useEffect, useCallback } from 'react'
import { Memory, FilterOptions } from '@/lib/types'
import SearchBar from '@/app/components/SearchBar'
import FilterPanel from '@/app/components/FilterPanel'
import MemoryList from '@/app/components/MemoryList'
import MemoryDetail from '@/app/components/MemoryDetail'

export default function Home() {
  const [memories, setMemories] = useState<Memory[]>([])
  const [filteredMemories, setFilteredMemories] = useState<Memory[]>([])
  const [selectedMemory, setSelectedMemory] = useState<Memory | null>(null)
  const [filters, setFilters] = useState<FilterOptions>({})
  const [loading, setLoading] = useState(true)

  // 加载所有记忆
  useEffect(() => {
    const loadMemories = async () => {
      try {
        const response = await fetch('/api/memories')
        const data = await response.json()
        setMemories(data)
        setFilteredMemories(data)
      } catch (error) {
        console.error('Failed to load memories:', error)
      } finally {
        setLoading(false)
      }
    }

    loadMemories()
  }, [])

  // 应用筛选
  useEffect(() => {
    const applyFilters = async () => {
      try {
        const response = await fetch('/api/search', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ memories, filters }),
        })
        const data = await response.json()
        setFilteredMemories(data)
      } catch (error) {
        console.error('Failed to filter memories:', error)
      }
    }

    applyFilters()
  }, [filters, memories])

  // 处理搜索
  const handleSearch = useCallback((query: string) => {
    setFilters(prev => ({ ...prev, searchQuery: query }))
  }, [])

  // 处理筛选
  const handleFilter = useCallback((newFilters: FilterOptions) => {
    setFilters(newFilters)
  }, [])

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
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-slate-100 mb-2">Second Brain</h1>
              <p className="text-slate-400">所有记忆和对话在一个地方</p>
            </div>
            <a
              href="/keywords"
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
            >
              关键词云
            </a>
          </div>
        </header>

        {/* 搜索栏 */}
        <div className="px-4 py-6 border-b border-slate-800">
          <SearchBar onSearch={handleSearch} />
        </div>

        {/* 主内容区 */}
        <div className="flex gap-6 p-4">
          {/* 左侧：筛选和列表 */}
          <div className="flex-1 min-w-0">
            <FilterPanel onFilter={handleFilter} />
            <MemoryList 
              memories={filteredMemories} 
              selectedId={selectedMemory?.id}
              onSelect={setSelectedMemory}
            />
          </div>

          {/* 右侧：详情 */}
          {selectedMemory && (
            <div className="w-96 border-l border-slate-800 pl-6">
              <MemoryDetail memory={selectedMemory} />
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
