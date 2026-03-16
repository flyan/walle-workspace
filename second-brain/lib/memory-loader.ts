import fs from 'fs'
import path from 'path'
import { Memory } from './types'

const AGENTS = ['main', 'coder', 'writer']

export async function loadAllMemories(): Promise<Memory[]> {
  const memories: Memory[] = []
  
  // 获取工作空间根目录
  const workspaceRoot = path.resolve(process.cwd(), '..')

  for (const agent of AGENTS) {
    const memoryPath = path.join(workspaceRoot, 'agents', agent, 'memory')
    
    if (!fs.existsSync(memoryPath)) {
      console.log(`Memory path not found: ${memoryPath}`)
      continue
    }

    const files = fs.readdirSync(memoryPath)
    
    for (const file of files) {
      if (!file.endsWith('.md')) continue

      const filePath = path.join(memoryPath, file)
      const content = fs.readFileSync(filePath, 'utf-8')
      
      const memory: Memory = {
        id: `${agent}-${file}`,
        title: file.replace('.md', ''),
        content,
        type: file.includes('reminder') ? 'memory' : 'note',
        agent: agent as any,
        date: extractDate(file),
        tags: extractTags(content),
        path: filePath,
      }
      
      memories.push(memory)
    }
  }

  console.log(`Loaded ${memories.length} memories`)
  return memories.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
}

function extractDate(filename: string): string {
  const match = filename.match(/(\d{4})-(\d{2})-(\d{2})/)
  if (match) {
    return `${match[1]}-${match[2]}-${match[3]}`
  }
  return new Date().toISOString().split('T')[0]
}

function extractTags(content: string): string[] {
  const tags = new Set<string>()
  const tagRegex = /#[\w\u4e00-\u9fa5]+/g
  const matches = content.match(tagRegex)
  if (matches) {
    matches.forEach(tag => tags.add(tag.substring(1)))
  }
  return Array.from(tags)
}
