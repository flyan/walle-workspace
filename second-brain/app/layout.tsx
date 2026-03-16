import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Second Brain',
  description: 'All memories and conversations in one place',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh-CN" className="dark">
      <body className="bg-slate-950 text-slate-100">
        {children}
      </body>
    </html>
  )
}
