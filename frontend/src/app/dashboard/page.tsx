'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/lib/auth'
import { UserRole, Project, Booking, Request } from '@/lib/types'
import api from '@/lib/api'
import Card from '@/components/Card'

export default function DashboardPage() {
  const router = useRouter()
  const { user, isAuthenticated } = useAuth()
  const [projects, setProjects] = useState<Project[]>([])
  const [bookings, setBookings] = useState<Booking[]>([])
  const [requests, setRequests] = useState<Request[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login')
      return
    }

    fetchData()
  }, [isAuthenticated, router])

  const fetchData = async () => {
    try {
      const [projectsRes, bookingsRes, requestsRes] = await Promise.all([
        api.get('/projects'),
        api.get('/bookings'),
        api.get('/requests'),
      ])

      setProjects(projectsRes.data)
      setBookings(bookingsRes.data)
      setRequests(requestsRes.data)
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  const openRequests = requests.filter(r => r.status === 'open')
  const upcomingBookings = bookings.filter(b => new Date(b.start_time) > new Date())

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-8">
        Bem-vindo, {user?.full_name}!
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Projetos</p>
              <p className="text-3xl font-bold text-gray-900">{projects.length}</p>
            </div>
            <div className="text-4xl">📁</div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Próximas Aulas</p>
              <p className="text-3xl font-bold text-gray-900">{upcomingBookings.length}</p>
            </div>
            <div className="text-4xl">📅</div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Solicitações Abertas</p>
              <p className="text-3xl font-bold text-gray-900">{openRequests.length}</p>
            </div>
            <div className="text-4xl">💬</div>
          </div>
        </Card>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Meus Projetos</h2>
          {projects.length === 0 ? (
            <p className="text-gray-500">Nenhum projeto encontrado</p>
          ) : (
            <ul className="space-y-2">
              {projects.slice(0, 5).map((project) => (
                <li
                  key={project.id}
                  onClick={() => router.push(`/projects/${project.id}`)}
                  className="p-3 bg-gray-50 rounded-lg hover:bg-gray-100 cursor-pointer transition-colors"
                >
                  <p className="font-medium text-gray-900">{project.name}</p>
                  <p className="text-sm text-gray-500">{project.status}</p>
                </li>
              ))}
            </ul>
          )}
        </Card>

        <Card>
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Próximas Aulas</h2>
          {upcomingBookings.length === 0 ? (
            <p className="text-gray-500">Nenhuma aula agendada</p>
          ) : (
            <ul className="space-y-2">
              {upcomingBookings.slice(0, 5).map((booking) => (
                <li key={booking.id} className="p-3 bg-gray-50 rounded-lg">
                  <p className="font-medium text-gray-900">{booking.title}</p>
                  <p className="text-sm text-gray-500">
                    {new Date(booking.start_time).toLocaleString('pt-BR')}
                  </p>
                </li>
              ))}
            </ul>
          )}
        </Card>
      </div>
    </div>
  )
}
