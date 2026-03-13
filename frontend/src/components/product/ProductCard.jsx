import { Plus, Minus, Clock, Star } from 'lucide-react'
import useCartStore from '../../store/cartStore'
import useAuthStore from '../../store/authStore'
import { useNavigate } from 'react-router-dom'

export default function ProductCard({ product }) {
  const { addToCart, updateQuantity, cart } = useCartStore()
  const { isAuthenticated } = useAuthStore()
  const navigate = useNavigate()

  const cartItem = cart?.items?.find(i => i.product_id === product.id)
  const qty = cartItem?.quantity || 0

  const handleAdd = (e) => {
    e.stopPropagation()
    if (!isAuthenticated) { navigate('/login'); return }
    addToCart(product.id, 1)
  }

  const handleUpdate = (e, newQty) => {
    e.stopPropagation()
    if (newQty <= 0) updateQuantity(cartItem.id, 0)
    else updateQuantity(cartItem.id, newQty)
  }

  const discount = product.discount || 0
  const savings = product.original_price ? product.original_price - product.price : 0

  return (
    <div className="card p-3 cursor-pointer group">
      {/* Image */}
      <div className="relative mb-3 rounded-xl overflow-hidden bg-gray-50 aspect-square">
        <img
          src={product.image_url || 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=300'}
          alt={product.name}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          onError={(e) => { e.target.src = 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=300' }}
        />
        {discount > 0 && (
          <span className="absolute top-2 left-2 bg-green-500 text-white text-xs font-bold px-2 py-0.5 rounded-full">
            {discount}% OFF
          </span>
        )}
        {!product.in_stock && (
          <div className="absolute inset-0 bg-white/80 flex items-center justify-center">
            <span className="text-gray-500 font-semibold text-sm">Out of Stock</span>
          </div>
        )}
      </div>

      {/* Info */}
      <div className="flex items-center gap-1 mb-1">
        <Clock className="w-3 h-3 text-purple-500" />
        <span className="text-xs text-purple-600 font-semibold">{product.delivery_time} mins</span>
        {product.rating && (
          <>
            <span className="text-gray-300 mx-1">·</span>
            <Star className="w-3 h-3 text-yellow-400 fill-yellow-400" />
            <span className="text-xs text-gray-500">{product.rating}</span>
          </>
        )}
      </div>

      <h3 className="font-semibold text-gray-800 text-sm leading-tight mb-0.5 line-clamp-2">{product.name}</h3>
      <p className="text-xs text-gray-400 mb-2">{product.unit}</p>

      {/* Price + Add */}
      <div className="flex items-center justify-between">
        <div>
          <span className="font-bold text-gray-900">₹{product.price}</span>
          {product.original_price && product.original_price > product.price && (
            <span className="text-xs text-gray-400 line-through ml-1">₹{product.original_price}</span>
          )}
        </div>

        {product.in_stock && (
          qty === 0 ? (
            <button onClick={handleAdd} className="flex items-center gap-1 bg-orange-500 hover:bg-orange-600 text-white text-sm font-bold px-3 py-1.5 rounded-xl transition-all active:scale-95">
              <Plus className="w-3.5 h-3.5" /> Add
            </button>
          ) : (
            <div className="flex items-center gap-2 bg-orange-50 rounded-xl p-1">
              <button onClick={(e) => handleUpdate(e, qty - 1)} className="qty-btn w-7 h-7">
                <Minus className="w-3 h-3" />
              </button>
              <span className="w-4 text-center font-bold text-orange-600 text-sm">{qty}</span>
              <button onClick={(e) => handleUpdate(e, qty + 1)} className="qty-btn w-7 h-7">
                <Plus className="w-3 h-3" />
              </button>
            </div>
          )
        )}
      </div>
    </div>
  )
}
