'use client'

import { KeywordStats } from '@/lib/keywords'

interface KeywordCloudProps {
  keywords: KeywordStats[]
  selectedKeyword?: string
  onSelect: (keyword: string) => void
}

export default function KeywordCloud({
  keywords,
  selectedKeyword,
  onSelect,
}: KeywordCloudProps) {
  if (keywords.length === 0) {
    return (
      <div className="text-center py-12 text-slate-400">
        没有关键词
      </div>
    )
  }

  return (
    <div className="flex flex-wrap gap-3 p-6 bg-slate-900 rounded-lg border border-slate-800">
      {keywords.map(kw => {
        // 根据重要性计算字体大小
        const minSize = 12
        const maxSize = 48
        const size = minSize + kw.importance * (maxSize - minSize)
        
        // 根据重要性计算颜色深度
        const opacity = 0.5 + kw.importance * 0.5

        return (
          <button
            key={kw.keyword}
            onClick={() => onSelect(kw.keyword)}
            className={`transition-all duration-200 ${
              selectedKeyword === kw.keyword
                ? 'text-blue-400 scale-110'
                : 'text-slate-300 hover:text-blue-300'
            }`}
            style={{
              fontSize: `${size}px`,
              opacity,
            }}
            title={`${kw.count} 次出现`}
          >
            {kw.keyword}
          </button>
        )
      })}
    </div>
  )
}
