import { searchMemories } from '@/lib/search'
import { Memory, FilterOptions } from '@/lib/types'
import { NextResponse } from 'next/server'

export async function POST(request: Request) {
  try {
    const { memories, filters } = await request.json()
    const filtered = searchMemories(memories, filters)
    return NextResponse.json(filtered)
  } catch (error) {
    console.error('Error searching memories:', error)
    return NextResponse.json(
      { error: 'Failed to search memories' },
      { status: 500 }
    )
  }
}
