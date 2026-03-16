import { loadAllMemories } from '@/lib/memory-loader'
import { NextResponse } from 'next/server'

export async function GET() {
  try {
    const memories = await loadAllMemories()
    return NextResponse.json(memories)
  } catch (error) {
    console.error('Error loading memories:', error)
    return NextResponse.json(
      { error: 'Failed to load memories' },
      { status: 500 }
    )
  }
}
