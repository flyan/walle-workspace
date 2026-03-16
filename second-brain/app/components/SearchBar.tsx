'use client'

import { useState, useEffect } from 'react'

interface SearchBarProps {
  onSearch: (query: string) => void
}

export default function SearchBar({ onSearch }: SearchBarProps) {
  const [query, setQuery] = useState('')

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault()
        const input = document.querySelector('input[type="search"]') as HTMLInputElement
        input?.focus()
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [])

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value
    setQuery(value)
    onSearch(value)
  }

  return (
    <div className="relative">
      <input
        type="search"
        placeholder="搜索记忆... (Cmd+K)"
        value={query}
        onChange={handleChange}
        className="search-input w-full"
      />
      <div className="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-500">
        ⌘K
      </div>
    </div>
  )
}
