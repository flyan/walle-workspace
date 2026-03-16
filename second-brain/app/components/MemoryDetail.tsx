'use client'

import { Memory } from '@/lib/types'

interface MemoryDetailProps {
  memory: Memory
}

export default function MemoryDetail({ memory }: MemoryDetailProps) {
  return (
    <div className="sticky top-4 max-h-[calc(100vh-2rem)] overflow-y-auto">
      <div className="space-y-4">
        {/* 标题 */}
        <div>
          <h2 className="text-2xl font-bold text-slate-100">
            {memory.title}
          </h2>
          <p className="text-sm text-slate-400 mt-1">
            {memory.date}
          </p>
        </div>

        {/* 元数据 */}
        <div className="flex flex-wrap gap-2">
          <span className="tag">
            {memory.agent === 'main' ? 'Walle' : memory.agent === 'coder' ? 'Coder' : 'Writer'}
          </span>
          <span className="tag">
            {memory.type === 'memory' ? '记忆' : memory.type === 'conversation' ? '对话' : '笔记'}
          </span>
        </div>

        {/* 标签 */}
        {memory.tags.length > 0 && (
          <div className="flex flex-wrap gap-2">
            {memory.tags.map(tag => (
              <span key={tag} className="tag bg-slate-700 text-slate-200">
                #{tag}
              </span>
            ))}
          </div>
        )}

        {/* 内容 */}
        <div className="prose prose-invert max-w-none">
          <div className="bg-slate-900 p-4 rounded-lg border border-slate-800">
            <div className="text-slate-300 whitespace-pre-wrap text-sm leading-relaxed">
              {memory.content}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
