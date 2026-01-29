'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/lib/auth'
import { File, UserRole } from '@/lib/types'
import api from '@/lib/api'
import Card from '@/components/Card'
import Button from '@/components/Button'

export default function FilesPage() {
  const router = useRouter()
  const { user, isAuthenticated } = useAuth()
  const [files, setFiles] = useState<File[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login')
      return
    }
    fetchFiles()
  }, [isAuthenticated, router])

  const fetchFiles = async () => {
    try {
      const response = await api.get('/files')
      setFiles(response.data)
    } catch (error) {
      console.error('Failed to fetch files:', error)
    } finally {
      setLoading(false)
    }
  }

  const formatFileSize = (bytes?: number) => {
    if (!bytes) return 'N/A'
    const mb = bytes / (1024 * 1024)
    if (mb < 1) {
      return `${(bytes / 1024).toFixed(2)} KB`
    }
    return `${mb.toFixed(2)} MB`
  }

  const handleDownload = async (fileId: number) => {
    try {
      const response = await api.get(`/files/${fileId}/download-url`)
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
        <h1 className="text-3xl font-bold text-gray-900">Arquivos</h1>
        {user?.role === UserRole.ADMIN && (
          <Button onClick={() => alert('Upload de arquivo (implementar)')}>
            + Novo Arquivo
          </Button>
        )}
      </div>

      {files.length === 0 ? (
        <Card>
          <p className="text-center text-gray-500 py-8">Nenhum arquivo encontrado</p>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {files.map((file) => (
            <Card key={file.id} className="hover:shadow-md transition-shadow">
              <div className="flex items-start justify-between mb-3">
                <div className="text-4xl">📄</div>
                <Button
                  size="sm"
                  variant="secondary"
                  onClick={() => handleDownload(file.id)}
                >
                  ⬇️
                </Button>
              </div>
              <h3 className="font-semibold text-gray-900 mb-1 truncate">{file.name}</h3>
              <p className="text-sm text-gray-600 mb-3 line-clamp-2">
                {file.description || 'Sem descrição'}
              </p>
              <div className="flex justify-between text-xs text-gray-500">
                <span>{formatFileSize(file.file_size_bytes)}</span>
                <span>{new Date(file.created_at).toLocaleDateString('pt-BR')}</span>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}
