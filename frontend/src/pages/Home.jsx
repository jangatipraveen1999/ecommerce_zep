import { useQuery } from '@tanstack/react-query'
import { Link, useNavigate } from 'react-router-dom'
import { Zap, ChevronRight, Clock, Shield, Tag } from 'lucide-react'
import api from '../utils/api'
import ProductCard from '../components/product/ProductCard'

export default function Home() {
  const navigate = useNavigate()

  const { data: categories = [] } = useQuery({
    queryKey: ['categories'],
    queryFn: () => api.get('/categories/').then(r => r.data)
  })

  const { data: products = [], isLoading } = useQuery({
    queryKey: ['products-home'],
    queryFn: () => api.get('/products/?limit=12').then(r => r.data)
  })

  const deals = products.filter(p => p.discount >= 15).slice(0, 8)

  return (
    <div className="max-w-7xl mx-auto px-4 py-6">

      {/* Hero */}
      <div className="relative bg-gradient-to-br from-orange-500 via-orange-400 to-amber-400 rounded-3xl p-8 mb-8 overflow-hidden">
        <div className="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full -translate-y-1/3 translate-x-1/4" />
        <div className="absolute bottom-0 left-1/2 w-48 h-48 bg-black/5 rounded-full translate-y-1/2" />
        <div className="relative z-10 max-w-lg">
          <div className="inline-flex items-center gap-2 bg-white/20 backdrop-blur-sm text-white text-sm font-semibold px-3 py-1.5 rounded-full mb-4">
            <Zap className="w-4 h-4 fill-white" /> Bengaluru's fastest delivery
          </div>
          <h1 className="text-4xl md:text-5xl font-black text-white mb-3 leading-tight" style={{ fontFamily: 'Plus Jakarta Sans' }}>
            Groceries in<br />
            <span className="text-yellow-200">10 minutes</span>
          </h1>
          <p className="text-white/90 text-lg mb-6">Fresh produce, dairy, snacks & more — delivered lightning fast.</p>
          <button onClick={() => navigate('/products')} className="bg-white text-orange-600 font-bold px-8 py-3.5 rounded-2xl hover:bg-orange-50 transition-colors text-base">
            Shop Now →
          </button>
        </div>
      </div>

      {/* Value Props */}
      <div className="grid grid-cols-3 gap-4 mb-8">
        {[
          { icon: Clock, label: '10 min delivery', sub: 'Lightning fast', color: 'bg-purple-50 text-purple-600' },
          { icon: Shield, label: 'Quality assured', sub: 'Fresh & safe', color: 'bg-green-50 text-green-600' },
          { icon: Tag, label: 'Best prices', sub: 'Guaranteed', color: 'bg-orange-50 text-orange-600' },
        ].map(({ icon: Icon, label, sub, color }) => (
          <div key={label} className="card p-4 flex items-center gap-3">
            <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${color}`}>
              <Icon className="w-5 h-5" />
            </div>
            <div>
              <p className="font-semibold text-gray-800 text-sm">{label}</p>
              <p className="text-xs text-gray-400">{sub}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Categories */}
      <section className="mb-8">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold text-gray-900" style={{ fontFamily: 'Plus Jakarta Sans' }}>Shop by Category</h2>
          <Link to="/products" className="text-orange-500 text-sm font-semibold hover:underline flex items-center gap-1">
            View all <ChevronRight className="w-4 h-4" />
          </Link>
        </div>
        <div className="grid grid-cols-4 md:grid-cols-8 gap-3">
          {categories.map(cat => (
            <Link key={cat.id} to={`/products?category=${cat.id}`}
              className="flex flex-col items-center gap-2 p-3 bg-white rounded-2xl border border-gray-100 hover:border-orange-200 hover:shadow-md transition-all group"
            >
              <div className="text-2xl">{cat.icon}</div>
              <span className="text-xs font-semibold text-gray-600 text-center leading-tight group-hover:text-orange-500">{cat.name}</span>
            </Link>
          ))}
        </div>
      </section>

      {/* Best Deals */}
      {deals.length > 0 && (
        <section className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <h2 className="text-xl font-bold text-gray-900" style={{ fontFamily: 'Plus Jakarta Sans' }}>🔥 Best Deals</h2>
              <span className="bg-red-100 text-red-600 text-xs font-bold px-2 py-0.5 rounded-full">Limited time</span>
            </div>
            <Link to="/products" className="text-orange-500 text-sm font-semibold hover:underline flex items-center gap-1">
              View all <ChevronRight className="w-4 h-4" />
            </Link>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-4">
            {deals.map(p => <ProductCard key={p.id} product={p} />)}
          </div>
        </section>
      )}

      {/* All Products */}
      <section>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold text-gray-900" style={{ fontFamily: 'Plus Jakarta Sans' }}>All Products</h2>
          <Link to="/products" className="text-orange-500 text-sm font-semibold hover:underline flex items-center gap-1">
            View all <ChevronRight className="w-4 h-4" />
          </Link>
        </div>
        {isLoading ? (
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
            {Array.from({ length: 12 }).map((_, i) => (
              <div key={i} className="bg-gray-100 rounded-2xl aspect-[3/4] animate-pulse" />
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
            {products.map(p => <ProductCard key={p.id} product={p} />)}
          </div>
        )}
      </section>
    </div>
  )
}
