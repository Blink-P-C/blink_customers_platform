'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useAuth } from '@/lib/auth'
import { UserRole } from '@/lib/types'

export default function Sidebar() {
  const pathname = usePathname()
  const { user, logout } = useAuth()

  const isActive = (path: string) => pathname === path

  const navItems = [
    { name: 'Dashboard', href: '/dashboard', icon: '📊' },
    { name: 'Projetos', href: '/projects', icon: '📁' },
    { name: 'Gravações', href: '/recordings', icon: '🎥' },
    { name: 'Arquivos', href: '/files', icon: '📄' },
    { name: 'Agendamentos', href: '/bookings', icon: '📅' },
    { name: 'Solicitações', href: '/requests', icon: '💬' },
  ]

  return (
    <div className="flex flex-col w-64 bg-white border-r border-gray-200">
      <div className="flex items-center justify-center h-16 border-b border-gray-200">
        <h1 className="text-xl font-bold text-primary-600">Blink Platform</h1>
      </div>

      <nav className="flex-1 px-4 py-6 space-y-2">
        {navItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className={`flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-colors ${
              isActive(item.href)
                ? 'bg-primary-50 text-primary-700'
                : 'text-gray-700 hover:bg-gray-50'
            }`}
          >
            <span className="mr-3 text-lg">{item.icon}</span>
            {item.name}
          </Link>
        ))}
      </nav>

      <div className="p-4 border-t border-gray-200">
        <div className="mb-3">
          <p className="text-sm font-medium text-gray-900">{user?.full_name}</p>
          <p className="text-xs text-gray-500">{user?.email}</p>
          {user?.role === UserRole.ADMIN && (
            <span className="inline-block px-2 py-1 mt-1 text-xs font-medium text-primary-700 bg-primary-100 rounded">
              Administrador
            </span>
          )}
        </div>
        <button
          onClick={logout}
          className="w-full px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-lg hover:bg-red-700 transition-colors"
        >
          Sair
        </button>
      </div>
    </div>
  )
}
