'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/lib/auth'
import { Project, UserRole } from '@/lib/types'
import api from '@/lib/api'
import Card from '@/components/Card'
import Button from '@/components/Button'

export default function ProjectsPage() {
  const router = useRouter()
  const { user, isAuthenticated } = useAuth()
  const [projects, setProjects] = useState<Project[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login')
      return
    }
    fetchProjects()
  }, [isAuthenticated, router])

  const fetchProjects = async () => {
    try {
      const response = await api.get('/projects')
      setProjects(response.data)
    } catch (error) {
      console.error('Failed to fetch projects:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="flex justify-center"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div></div>
  }

  const statusColors: Record<string, string> = {
    active: 'bg-green-100 text-green-800',
    completed: 'bg-blue-100 text-blue-800',
    on_hold: 'bg-yellow-100 text-yellow-800',
    cancelled: 'bg-red-100 text-red-800',
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Projetos</h1>
        {user?.role === UserRole.ADMIN && (
          <Button onClick={() => alert('Criar projeto (implementar modal)')}>
            + Novo Projeto
          </Button>
        )}
      </div>

      {projects.length === 0 ? (
        <Card>
          <p className="text-center text-gray-500 py-8">Nenhum projeto encontrado</p>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.map((project) => (
            <Card
              key={project.id}
              className="cursor-pointer hover:shadow-md transition-shadow"
              onClick={() => router.push(`/projects/${project.id}`)}
            >
              <div className="flex justify-between items-start mb-3">
                <h3 className="text-lg font-semibold text-gray-900">{project.name}</h3>
                <span className={`px-2 py-1 text-xs font-medium rounded ${statusColors[project.status]}`}>
                  {project.status}
                </span>
              </div>
              <p className="text-sm text-gray-600 mb-4 line-clamp-2">
                {project.description || 'Sem descrição'}
              </p>
              <div className="text-xs text-gray-500">
                Criado em {new Date(project.created_at).toLocaleDateString('pt-BR')}
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}
