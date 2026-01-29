'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/lib/auth'
import { Booking, AvailabilitySlot, UserRole } from '@/lib/types'
import api from '@/lib/api'
import Card from '@/components/Card'
import Button from '@/components/Button'
import Modal from '@/components/Modal'

export default function BookingsPage() {
  const router = useRouter()
  const { user, isAuthenticated } = useAuth()
  const [bookings, setBookings] = useState<Booking[]>([])
  const [slots, setSlots] = useState<AvailabilitySlot[]>([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login')
      return
    }
    fetchData()
  }, [isAuthenticated, router])

  const fetchData = async () => {
    try {
      const [bookingsRes, slotsRes] = await Promise.all([
        api.get('/bookings'),
        api.get('/bookings/slots'),
      ])
      setBookings(bookingsRes.data)
      setSlots(slotsRes.data)
    } catch (error) {
      console.error('Failed to fetch data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleBookSlot = async (slotId: number) => {
    const title = prompt('Título da aula:')
    if (!title) return

    const description = prompt('Descrição (opcional):')

    try {
      await api.post('/bookings', {
        slot_id: slotId,
        title,
        description,
      })
      alert('Aula agendada com sucesso!')
      fetchData()
      setShowModal(false)
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Erro ao agendar aula')
    }
  }

  const handleCancelBooking = async (bookingId: number) => {
    if (!confirm('Tem certeza que deseja cancelar este agendamento?')) return

    try {
      await api.delete(`/bookings/${bookingId}`)
      alert('Agendamento cancelado')
      fetchData()
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Erro ao cancelar agendamento')
    }
  }

  if (loading) {
    return <div className="flex justify-center"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div></div>
  }

  const upcomingBookings = bookings.filter(b => new Date(b.start_time) > new Date())
  const pastBookings = bookings.filter(b => new Date(b.start_time) <= new Date())

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Agendamentos</h1>
        {user?.role === UserRole.CLIENT && (
          <Button onClick={() => setShowModal(true)}>
            📅 Agendar Aula
          </Button>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div>
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Próximas Aulas</h2>
          {upcomingBookings.length === 0 ? (
            <Card>
              <p className="text-gray-500 text-center py-4">Nenhuma aula agendada</p>
            </Card>
          ) : (
            <div className="space-y-3">
              {upcomingBookings.map((booking) => (
                <Card key={booking.id}>
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <h3 className="font-semibold text-gray-900">{booking.title}</h3>
                      <p className="text-sm text-gray-600 mt-1">{booking.description}</p>
                      <p className="text-sm text-gray-500 mt-2">
                        📅 {new Date(booking.start_time).toLocaleString('pt-BR')}
                      </p>
                      {booking.meeting_link && (
                        <a
                          href={booking.meeting_link}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-sm text-primary-600 hover:underline mt-2 inline-block"
                        >
                          🔗 Link da reunião
                        </a>
                      )}
                    </div>
                    <Button
                      size="sm"
                      variant="danger"
                      onClick={() => handleCancelBooking(booking.id)}
                    >
                      Cancelar
                    </Button>
                  </div>
                </Card>
              ))}
            </div>
          )}
        </div>

        <div>
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Aulas Anteriores</h2>
          {pastBookings.length === 0 ? (
            <Card>
              <p className="text-gray-500 text-center py-4">Nenhuma aula anterior</p>
            </Card>
          ) : (
            <div className="space-y-3">
              {pastBookings.slice(0, 5).map((booking) => (
                <Card key={booking.id} className="opacity-75">
                  <h3 className="font-semibold text-gray-900">{booking.title}</h3>
                  <p className="text-sm text-gray-500 mt-1">
                    📅 {new Date(booking.start_time).toLocaleString('pt-BR')}
                  </p>
                </Card>
              ))}
            </div>
          )}
        </div>
      </div>

      <Modal isOpen={showModal} onClose={() => setShowModal(false)} title="Agendar Aula">
        <div className="space-y-3">
          <p className="text-sm text-gray-600 mb-4">Selecione um horário disponível:</p>
          {slots.length === 0 ? (
            <p className="text-gray-500 text-center py-4">Nenhum horário disponível</p>
          ) : (
            slots.map((slot) => (
              <div
                key={slot.id}
                className="flex justify-between items-center p-3 bg-gray-50 rounded-lg hover:bg-gray-100 cursor-pointer"
                onClick={() => handleBookSlot(slot.id)}
              >
                <div>
                  <p className="font-medium text-gray-900">
                    {new Date(slot.start_time).toLocaleString('pt-BR')}
                  </p>
                  <p className="text-sm text-gray-500">
                    até {new Date(slot.end_time).toLocaleTimeString('pt-BR')}
                  </p>
                </div>
                <Button size="sm">Agendar</Button>
              </div>
            ))
          )}
        </div>
      </Modal>
    </div>
  )
}
