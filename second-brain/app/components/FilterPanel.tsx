'use client'

import { useState } from 'react'
import { FilterOptions } from '@/lib/types'

interface FilterPanelProps {
  onFilter: (filters: FilterOptions) => void
}

export default function FilterPanel({ onFilter }: FilterPanelProps) {
  const [type, setType] = useState<string>('')
  const [agent, setAgent] = useState<string>('')

  const handleTypeChange = (newType: string) => {
    setType(newType)
    onFilter({ type: newType || undefined, agent: agent || undefined })
  }

  const handleAgentChange = (newAgent: string) => {
    setAgent(newAgent)
    onFilter({ type: type || undefined, agent: newAgent || undefined })
  }

  return (
    <div className="mb-6 space-y-4">
      {/* 类型筛选 */}
      <div>
        <h3 className="text-sm font-semibold text-slate-300 mb-2">类型</h3>
        <div className="space-y-2">
          {['memory', 'conversation', 'note'].map(t => (
            <label key={t} className="flex items-center gap-2 cursor-pointer">
              <input
                type="radio"
                name="type"
                value={t}
                checked={type === t}
                onChange={e => handleTypeChange(e.target.value)}
                className="w-4 h-4"
              />
              <span className="text-sm text-slate-400">
                {t === 'memory' ? '记忆' : t === 'conversation' ? '对话' : '笔记'}
              </span>
            </label>
          ))}
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="radio"
              name="type"
              value=""
              checked={type === ''}
              onChange={e => handleTypeChange(e.target.value)}
              className="w-4 h-4"
            />
            <span className="text-sm text-slate-400">全部</span>
          </label>
        </div>
      </div>

      {/* Agent 筛选 */}
      <div>
        <h3 className="text-sm font-semibold text-slate-300 mb-2">Agent</h3>
        <div className="space-y-2">
          {['main', 'coder', 'writer'].map(a => (
            <label key={a} className="flex items-center gap-2 cursor-pointer">
              <input
                type="radio"
                name="agent"
                value={a}
                checked={agent === a}
                onChange={e => handleAgentChange(e.target.value)}
                className="w-4 h-4"
              />
              <span className="text-sm text-slate-400">
                {a === 'main' ? 'Walle' : a === 'coder' ? 'Coder' : 'Writer'}
              </span>
            </label>
          ))}
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="radio"
              name="agent"
              value=""
              checked={agent === ''}
              onChange={e => handleAgentChange(e.target.value)}
              className="w-4 h-4"
            />
            <span className="text-sm text-slate-400">全部</span>
          </label>
        </div>
      </div>
    </div>
  )
}
