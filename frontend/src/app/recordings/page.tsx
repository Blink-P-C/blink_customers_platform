'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/lib/auth'
import { Recording, UserRole } from '@/lib/types'
import api from '@/lib/api'
import Card from '@/components/Card'
import Button from '@/components/Button'

export default function RecordingsPage() {
  const router = useRouter()
  const { user, isAuthenticated } = useAuth()
  const [recordings, setRecordings] = useState<Recording[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login')
      return
    }
    fetchRecordings()
  }, [isAuthenticated, router])

  const fetchRecordings = async () => {
    try {
      const response = await api.get('/recordings')
      setRecordings(response.data)
    } catch (error) {
      console.error('Failed to fetch recordings:', error)
    } finally {
      setLoading(false)
    }
  }

  const formatFileSize = (bytes?: number) => {
    if (!bytes) return 'N/A'
    const mb = bytes / (1024 * 1024)
    return `${mb.toFixed(2)} MB`
  }

  const formatDuration = (seconds?: number) => {
    if (!seconds) return 'N/A'
    const minutes = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${minutes}:${secs.toString().padStart(2, '0')}`
  }

  const handleDownload = async (recordingId: number) => {
    try {
      const response = await api.get(`/recordings/${recordingId}/download-url`)
      window.open(response.data.download_url, '_blank')
    } catch (error) {
      console.error('Failed to get download URL:', error)
      alert('Erro ao obter link de download')
    }
  }

  if (loading) {
    return <div className="flex justify-center"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div></div>
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Gravações</h1>
        {user?.role === UserRole.ADMIN && (
          <Button onClick={() => alert('Upload de gravação (implementar)')}>
            + Nova Gravação
          </Button>
        )}
      </div>

      {recordings.length === 0 ? (
        <Card>
          <p className="text-center text-gray-500 py-8">Nenhuma gravação encontrada</p>
        </Card>
      ) : (
        <div className="space-y-4">
          {recordings.map((recording) => (
            <Card key={recording.id}>
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">{recording.title}</h3>
                  <p className="text-sm text-gray-600 mb-3">{recording.description}</p>
                  <div className="flex gap-4 text-sm text-gray-500">
                    <span>📦 {formatFileSize(recording.file_size_bytes)}</span>
                    {recording.duration_seconds && (
                      <span>⏱️ {formatDuration(recording.duration_seconds)}</span>
                    )}
                    <span>📅 {new Date(recording.created_at).toLocaleDateString('pt-BR')}</span>
                  </div>
                </div>
                <Button
                  size="sm"
                  onClick={() => handleDownload(recording.id)}
                >
                  📥 Assistir
                </Button>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}
