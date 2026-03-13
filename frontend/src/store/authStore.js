import { create } from 'zustand'
import api from '../utils/api'

const useAuthStore = create((set) => ({
  user: JSON.parse(localStorage.getItem('zapkart_user') || 'null'),
  token: localStorage.getItem('zapkart_token') || null,
  isAuthenticated: !!localStorage.getItem('zapkart_token'),

  login: async (email, password) => {
    const res = await api.post('/auth/login', { email, password })
    const { access_token, user } = res.data
    localStorage.setItem('zapkart_token', access_token)
    localStorage.setItem('zapkart_user', JSON.stringify(user))
    set({ user, token: access_token, isAuthenticated: true })
    return user
  },

  register: async (data) => {
    const res = await api.post('/auth/register', data)
    const { access_token, user } = res.data
    localStorage.setItem('zapkart_token', access_token)
    localStorage.setItem('zapkart_user', JSON.stringify(user))
    set({ user, token: access_token, isAuthenticated: true })
    return user
  },

  logout: () => {
    localStorage.removeItem('zapkart_token')
    localStorage.removeItem('zapkart_user')
    set({ user: null, token: null, isAuthenticated: false })
  },
}))

export default useAuthStore
