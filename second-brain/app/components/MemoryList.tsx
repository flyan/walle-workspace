'use client'

import { Memory } from '@/lib/types'

interface MemoryListProps {
  memories: Memory[]
  selectedId?: string
  onSelect: (memory: Memory) => void
}

export default function MemoryList({ memories, selectedId, onSelect }: MemoryListProps) {
  if (memories.length === 0) {
    return (
      <div className="text-center py-12 text-slate-400">
        没有找到匹配的记忆
      </div>
    )
  }

  return (
    <div className="space-y-2">
      {memories.map(memory => (
        <div
          key={memory.id}
          onClick={() => onSelect(memory)}
          className={`memory-card cursor-pointer ${
            selectedId === memory.id ? 'border-blue-500 bg-slate-800' : ''
          }`}
        >
          <div className="flex items-start justify-between gap-2">
            <div className="flex-1 min-w-0">
              <h3 className="font-semibold text-slate-100 truncate">
                {memory.title}
              </h3>
              <p className="text-sm text-slate-400 line-clamp-2 mt-1">
                {memory.content.substring(0, 100)}...
              </p>
            </div>
            <span className="text-xs text-slate-500 whitespace-nowrap">
              {memory.date}
            </span>
          </div>
          
          <div className="flex items-center gap-2 mt-3">
            <span className="tag">
              {memory.agent === 'main' ? 'Walle' : memory.agent === 'coder' ? 'Coder' : 'Writer'}
            </span>
            <span className="tag">
              {memory.type === 'memory' ? '记忆' : memory.type === 'conversation' ? '对话' : '笔记'}
            </span>
          </div>
        </div>
      ))}
    </div>
  )
}
