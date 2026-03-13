import { Link, useNavigate } from 'react-router-dom'
import { ShoppingCart, Zap, MapPin, User, Package, LogOut, Search } from 'lucide-react'
import useAuthStore from '../../store/authStore'
import useCartStore from '../../store/cartStore'
import { useState } from 'react'

export default function Navbar() {
  const { isAuthenticated, user, logout } = useAuthStore()
  const { cart } = useCartStore()
  const navigate = useNavigate()
  const [search, setSearch] = useState('')
  const [showMenu, setShowMenu] = useState(false)
  const totalItems = cart?.total_items || 0

  const handleSearch = (e) => {
    e.preventDefault()
    if (search.trim()) navigate(`/products?search=${encodeURIComponent(search.trim())}`)
  }

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-white border-b border-gray-100 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 h-16 flex items-center gap-4">
        {/* Logo */}
        <Link to="/" className="flex items-center gap-1.5 shrink-0">
          <div className="w-8 h-8 bg-orange-500 rounded-lg flex items-center justify-center">
            <Zap className="w-5 h-5 text-white fill-white" />
          </div>
          <span className="text-xl font-extrabold text-gray-900" style={{ fontFamily: 'Plus Jakarta Sans' }}>
            Zap<span className="text-orange-500">Kart</span>
          </span>
        </Link>

        {/* Delivery badge */}
        <div className="hidden md:flex items-center gap-1.5 bg-purple-50 border border-purple-100 rounded-xl px-3 py-1.5 shrink-0">
          <MapPin className="w-3.5 h-3.5 text-purple-600" />
          <span className="text-xs font-semibold text-purple-700">Delivery in</span>
          <span className="text-xs font-black text-purple-900">10 mins</span>
        </div>

        {/* Search */}
        <form onSubmit={handleSearch} className="flex-1 max-w-xl">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search for groceries, snacks..."
              className="w-full pl-9 pr-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-transparent"
            />
          </div>
        </form>

        {/* Right side */}
        <div className="flex items-center gap-2 ml-auto shrink-0">
          {isAuthenticated ? (
            <>
              <div className="relative">
                <button onClick={() => setShowMenu(!showMenu)} className="flex items-center gap-2 px-3 py-2 rounded-xl hover:bg-gray-50 transition-colors">
                  <div className="w-7 h-7 bg-orange-100 rounded-full flex items-center justify-center">
                    <User className="w-4 h-4 text-orange-600" />
                  </div>
                  <span className="hidden md:block text-sm font-semibold text-gray-700">{user?.name?.split(' ')[0]}</span>
                </button>
                {showMenu && (
                  <div className="absolute right-0 top-12 w-48 bg-white rounded-2xl shadow-xl border border-gray-100 py-2 z-50">
                    <Link to="/orders" onClick={() => setShowMenu(false)} className="flex items-center gap-2 px-4 py-2.5 text-sm text-gray-700 hover:bg-gray-50">
                      <Package className="w-4 h-4" /> My Orders
                    </Link>
                    <button onClick={() => { logout(); setShowMenu(false) }} className="flex items-center gap-2 px-4 py-2.5 text-sm text-red-500 hover:bg-red-50 w-full">
                      <LogOut className="w-4 h-4" /> Logout
                    </button>
                  </div>
                )}
              </div>
              <Link to="/cart" className="relative flex items-center gap-2 bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-xl font-semibold text-sm transition-colors">
                <ShoppingCart className="w-4 h-4" />
                <span className="hidden md:block">Cart</span>
                {totalItems > 0 && (
                  <span className="absolute -top-2 -right-2 w-5 h-5 bg-green-500 rounded-full text-xs font-bold flex items-center justify-center">{totalItems}</span>
                )}
              </Link>
            </>
          ) : (
            <>
              <Link to="/login" className="text-sm font-semibold text-gray-700 hover:text-orange-500 px-3 py-2 rounded-xl hover:bg-orange-50 transition-colors">Login</Link>
              <Link to="/register" className="btn-primary text-sm py-2 px-4">Sign Up</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  )
}
