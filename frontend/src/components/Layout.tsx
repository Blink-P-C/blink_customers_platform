'use client'

import { ReactNode } from 'react'
import Sidebar from './Sidebar'
import { useAuth } from '@/lib/auth'

interface LayoutProps {
  children: ReactNode
}

export default function Layout({ children }: LayoutProps) {
  const { user } = useAuth()

  if (!user) {
    return <>{children}</>
  }

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar />
      <main className="flex-1 overflow-y-auto p-8">
        {children}
      </main>
    </div>
  )
}
