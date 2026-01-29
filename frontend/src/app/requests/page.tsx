'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/lib/auth'
import { Request, RequestType, UserRole, Project } from '@/lib/types'
import api from '@/lib/api'
import Card from '@/components/Card'
import Button from '@/components/Button'
import Modal from '@/components/Modal'
import Input from '@/components/Input'

export default function RequestsPage() {
  const router = useRouter()
  const { user, isAuthenticated } = useAuth()
  const [requests, setRequests] = useState<Request[]>([])
  const [projects, setProjects] = useState<Project[]>([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [formData, setFormData] = useState({
    project_id: 0,
    title: '',
    description: '',
    type: RequestType.QUESTION,
  })

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login')
      return
    }
    fetchData()
  }, [isAuthenticated, router])

  const fetchData = async () => {
    try {
      const [requestsRes, projectsRes] = await Promise.all([
        api.get('/requests'),
        api.get('/projects'),
      ])
      setRequests(requestsRes.data)
      setProjects(projectsRes.data)
    } catch (error) {
      console.error('Failed to fetch data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await api.post('/requests', formData)
      alert('Solicitação criada com sucesso!')
      setShowModal(false)
      setFormData({
        project_id: 0,
        title: '',
        description: '',
        type: RequestType.QUESTION,
      })
      fetchData()
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Erro ao criar solicitação')
    }
  }

  if (loading) {
    return <div className="flex justify-center"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div></div>
  }

  const statusColors: Record<string, string> = {
    open: 'bg-yellow-100 text-yellow-800',
    in_progress: 'bg-blue-100 text-blue-800',
    completed: 'bg-green-100 text-green-800',
    cancelled: 'bg-red-100 text-red-800',
  }

  const typeLabels: Record<string, string> = {
    improvement: 'Melhoria',
    revision: 'Revisão',
    bug: 'Bug',
    question: 'Dúvida',
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Solicitações</h1>
        <Button onClick={() => setShowModal(true)}>
          + Nova Solicitação
        </Button>
      </div>

      {requests.length === 0 ? (
        <Card>
          <p className="text-center text-gray-500 py-8">Nenhuma solicitação encontrada</p>
        </Card>
      ) : (
        <div className="space-y-4">
          {requests.map((request) => (
            <Card
              key={request.id}
              className="cursor-pointer hover:shadow-md transition-shadow"
              onClick={() => router.push(`/requests/${request.id}`)}
            >
              <div className="flex justify-between items-start mb-3">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <h3 className="text-lg font-semibold text-gray-900">{request.title}</h3>
                    <span className={`px-2 py-1 text-xs font-medium rounded ${statusColors[request.status]}`}>
                      {request.status}
                    </span>
                    <span className="px-2 py-1 text-xs font-medium bg-gray-100 text-gray-700 rounded">
                      {typeLabels[request.type]}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mb-2 line-clamp-2">{request.description}</p>
                  <div className="flex gap-4 text-xs text-gray-500">
                    <span>💬 {request.messages?.length || 0} mensagens</span>
                    <span>📅 {new Date(request.created_at).toLocaleDateString('pt-BR')}</span>
                  </div>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}

      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title="Nova Solicitação">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Projeto</label>
            <select
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              value={formData.project_id}
              onChange={(e) => setFormData({ ...formData, project_id: parseInt(e.target.value) })}
              required
            >
              <option value={0}>Selecione um projeto</option>
              {projects.map((project) => (
                <option key={project.id} value={project.id}>
                  {project.name}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Tipo</label>
            <select
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              value={formData.type}
              onChange={(e) => setFormData({ ...formData, type: e.target.value as RequestType })}
              required
            >
              <option value={RequestType.QUESTION}>Dúvida</option>
              <option value={RequestType.IMPROVEMENT}>Melhoria</option>
              <option value={RequestType.REVISION}>Revisão</option>
              <option value={RequestType.BUG}>Bug</option>
            </select>
          </div>

          <Input
            label="Título"
            placeholder="Título da solicitação"
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            required
          />

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Descrição</label>
            <textarea
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              rows={4}
              placeholder="Descreva sua solicitação..."
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              required
            />
          </div>

          <div className="flex gap-3">
            <Button type="submit" className="flex-1">
              Criar Solicitação
            </Button>
            <Button type="button" variant="secondary" onClick={() => setShowModal(false)}>
              Cancelar
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  )
}
