import { Outlet } from 'react-router-dom'
import Navbar from './Navbar'
import { useEffect } from 'react'
import useCartStore from '../../store/cartStore'
import useAuthStore from '../../store/authStore'

export default function Layout() {
  const { isAuthenticated } = useAuthStore()
  const { fetchCart } = useCartStore()

  useEffect(() => {
    if (isAuthenticated) fetchCart()
  }, [isAuthenticated])

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main className="pt-16">
        <Outlet />
      </main>
    </div>
  )
}
