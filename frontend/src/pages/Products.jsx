import { useQuery } from '@tanstack/react-query'
import { useSearchParams } from 'react-router-dom'
import { Search, SlidersHorizontal } from 'lucide-react'
import { useState, useEffect } from 'react'
import api from '../utils/api'
import ProductCard from '../components/product/ProductCard'

export default function Products() {
  const [searchParams, setSearchParams] = useSearchParams()
  const [search, setSearch] = useState(searchParams.get('search') || '')
  const categoryId = searchParams.get('category')

  const { data: categories = [] } = useQuery({
    queryKey: ['categories'],
    queryFn: () => api.get('/categories/').then(r => r.data)
  })

  const { data: products = [], isLoading } = useQuery({
    queryKey: ['products', search, categoryId],
    queryFn: () => {
      const params = new URLSearchParams()
      if (search) params.set('search', search)
      if (categoryId) params.set('category_id', categoryId)
      params.set('limit', '100')
      return api.get(`/products/?${params}`).then(r => r.data)
    }
  })

  const handleCategoryClick = (id) => {
    const params = new URLSearchParams(searchParams)
    if (id === null) params.delete('category')
    else params.set('category', id)
    setSearchParams(params)
  }

  const handleSearch = (e) => {
    e.preventDefault()
    const params = new URLSearchParams(searchParams)
    if (search.trim()) params.set('search', search.trim())
    else params.delete('search')
    setSearchParams(params)
  }

  const selectedCat = categories.find(c => c.id === Number(categoryId))

  return (
    <div className="max-w-7xl mx-auto px-4 py-6">
      <div className="flex gap-6">
        {/* Sidebar */}
        <aside className="hidden md:block w-56 shrink-0">
          <div className="card p-4 sticky top-20">
            <h3 className="font-bold text-gray-800 mb-3">Categories</h3>
            <button onClick={() => handleCategoryClick(null)}
              className={`w-full text-left px-3 py-2 rounded-xl text-sm font-medium transition-colors mb-1 ${!categoryId ? 'bg-orange-100 text-orange-700' : 'hover:bg-gray-50 text-gray-600'}`}>
              All Products
            </button>
            {categories.map(cat => (
              <button key={cat.id} onClick={() => handleCategoryClick(cat.id)}
                className={`w-full text-left px-3 py-2 rounded-xl text-sm font-medium transition-colors mb-1 flex items-center gap-2 ${Number(categoryId) === cat.id ? 'bg-orange-100 text-orange-700' : 'hover:bg-gray-50 text-gray-600'}`}>
                <span>{cat.icon}</span> {cat.name}
              </button>
            ))}
          </div>
        </aside>

        {/* Main */}
        <div className="flex-1">
          {/* Header */}
          <div className="flex items-center justify-between mb-5">
            <div>
              <h1 className="text-2xl font-bold text-gray-900" style={{ fontFamily: 'Plus Jakarta Sans' }}>
                {selectedCat ? `${selectedCat.icon} ${selectedCat.name}` : 'All Products'}
              </h1>
              <p className="text-sm text-gray-500">{products.length} items</p>
            </div>
            <form onSubmit={handleSearch} className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input value={search} onChange={e => setSearch(e.target.value)}
                placeholder="Search products..."
                className="pl-9 pr-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-orange-400 w-56"
              />
            </form>
          </div>

          {/* Mobile categories */}
          <div className="flex gap-2 mb-4 overflow-x-auto pb-2 md:hidden">
            <button onClick={() => handleCategoryClick(null)}
              className={`shrink-0 px-3 py-1.5 rounded-full text-sm font-medium ${!categoryId ? 'bg-orange-500 text-white' : 'bg-white border text-gray-600'}`}>
              All
            </button>
            {categories.map(cat => (
              <button key={cat.id} onClick={() => handleCategoryClick(cat.id)}
                className={`shrink-0 px-3 py-1.5 rounded-full text-sm font-medium flex items-center gap-1 ${Number(categoryId) === cat.id ? 'bg-orange-500 text-white' : 'bg-white border text-gray-600'}`}>
                {cat.icon} {cat.name}
              </button>
            ))}
          </div>

          {isLoading ? (
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {Array.from({ length: 12 }).map((_, i) => <div key={i} className="bg-gray-100 rounded-2xl aspect-[3/4] animate-pulse" />)}
            </div>
          ) : products.length === 0 ? (
            <div className="text-center py-20">
              <p className="text-6xl mb-4">🔍</p>
              <h3 className="font-bold text-gray-800 text-xl mb-2">No products found</h3>
              <p className="text-gray-500">Try a different search or category</p>
            </div>
          ) : (
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {products.map(p => <ProductCard key={p.id} product={p} />)}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
