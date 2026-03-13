import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import Layout from './components/layout/Layout'
import Home from './pages/Home'
import Products from './pages/Products'
import Cart from './pages/Cart'
import Checkout from './pages/Checkout'
import Orders from './pages/Orders'
import Login from './pages/Login'
import Register from './pages/Register'
import useAuthStore from './store/authStore'

const queryClient = new QueryClient()

function ProtectedRoute({ children }) {
  const { isAuthenticated } = useAuthStore()
  return isAuthenticated ? children : <Navigate to="/login" replace />
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Toaster position="top-center" toastOptions={{ style: { fontFamily: 'DM Sans', borderRadius: '12px' } }} />
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/" element={<Layout />}>
            <Route index element={<Home />} />
            <Route path="products" element={<Products />} />
            <Route path="cart" element={<ProtectedRoute><Cart /></ProtectedRoute>} />
            <Route path="checkout" element={<ProtectedRoute><Checkout /></ProtectedRoute>} />
            <Route path="orders" element={<ProtectedRoute><Orders /></ProtectedRoute>} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  )
}
