import { create } from 'zustand'
import api from '../utils/api'
import toast from 'react-hot-toast'

const useCartStore = create((set, get) => ({
  cart: null,
  loading: false,

  fetchCart: async () => {
    try {
      set({ loading: true })
      const res = await api.get('/cart/')
      set({ cart: res.data })
    } catch (e) {
      set({ cart: null })
    } finally {
      set({ loading: false })
    }
  },

  addToCart: async (productId, quantity = 1) => {
    try {
      await api.post('/cart/add', { product_id: productId, quantity })
      await get().fetchCart()
      toast.success('Added to cart! 🛒', { duration: 1500 })
    } catch {
      toast.error('Please login to add items')
    }
  },

  updateQuantity: async (itemId, quantity) => {
    try {
      await api.put(`/cart/${itemId}`, { quantity })
      await get().fetchCart()
    } catch {
      toast.error('Failed to update cart')
    }
  },

  removeItem: async (itemId) => {
    try {
      await api.delete(`/cart/${itemId}`)
      await get().fetchCart()
      toast.success('Item removed')
    } catch {
      toast.error('Failed to remove item')
    }
  },

  clearCart: async () => {
    try {
      await api.delete('/cart/')
      set({ cart: null })
    } catch {}
  },

  get totalItems() {
    return get().cart?.total_items || 0
  },
}))

export default useCartStore
