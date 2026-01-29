import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import api from './api'
import { User } from './types'

interface AuthState {
  user: User | null
  isAuthenticated: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  fetchUser: () => Promise<void>
}

export const useAuth = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      isAuthenticated: false,

      login: async (email: string, password: string) => {
        const formData = new FormData()
        formData.append('username', email) // OAuth2 uses 'username' field
        formData.append('password', password)

        const response = await api.post('/auth/login', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })

        const { access_token, refresh_token } = response.data
        localStorage.setItem('access_token', access_token)
        localStorage.setItem('refresh_token', refresh_token)

        // Fetch user data
        const userResponse = await api.get('/auth/me')
        set({ user: userResponse.data, isAuthenticated: true })
      },

      logout: () => {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        set({ user: null, isAuthenticated: false })
      },

      fetchUser: async () => {
        try {
          const response = await api.get('/auth/me')
          set({ user: response.data, isAuthenticated: true })
        } catch (error) {
          set({ user: null, isAuthenticated: false })
        }
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
)
