import { Link, useNavigate } from 'react-router-dom'
import { Minus, Plus, Trash2, ShoppingBag, ArrowRight, Clock } from 'lucide-react'
import useCartStore from '../store/cartStore'

export default function Cart() {
  const { cart, updateQuantity, removeItem, loading } = useCartStore()
  const navigate = useNavigate()

  if (loading) return <div className="flex items-center justify-center h-64"><div className="animate-spin w-8 h-8 border-4 border-orange-500 border-t-transparent rounded-full" /></div>

  if (!cart || cart.items.length === 0) {
    return (
      <div className="max-w-md mx-auto text-center py-20 px-4">
        <div className="text-8xl mb-6">🛒</div>
        <h2 className="text-2xl font-bold text-gray-800 mb-2" style={{ fontFamily: 'Plus Jakarta Sans' }}>Your cart is empty</h2>
        <p className="text-gray-500 mb-8">Add some delicious items to get started!</p>
        <Link to="/products" className="btn-primary inline-flex items-center gap-2">
          <ShoppingBag className="w-4 h-4" /> Browse Products
        </Link>
      </div>
    )
  }

  return (
    <div className="max-w-5xl mx-auto px-4 py-6">
      <h1 className="text-2xl font-bold text-gray-900 mb-6" style={{ fontFamily: 'Plus Jakarta Sans' }}>
        My Cart <span className="text-gray-400 font-normal">({cart.total_items} items)</span>
      </h1>

      <div className="grid md:grid-cols-[1fr_360px] gap-6">
        {/* Items */}
        <div className="space-y-3">
          {/* Delivery badge */}
          <div className="flex items-center gap-2 bg-purple-50 border border-purple-100 rounded-2xl px-4 py-3">
            <Clock className="w-4 h-4 text-purple-600" />
            <span className="text-sm font-semibold text-purple-800">Delivery in 10 minutes 🚀</span>
          </div>

          {cart.items.map(item => (
            <div key={item.id} className="card p-4 flex items-center gap-4">
              <img src={item.product.image_url} alt={item.product.name}
                className="w-16 h-16 rounded-xl object-cover bg-gray-50 shrink-0"
                onError={e => e.target.src = 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=100'} />
              <div className="flex-1 min-w-0">
                <h3 className="font-semibold text-gray-800 text-sm truncate">{item.product.name}</h3>
                <p className="text-xs text-gray-400">{item.product.unit}</p>
                <p className="font-bold text-gray-900 mt-1">₹{item.product.price}</p>
              </div>
              <div className="flex items-center gap-2">
                <button onClick={() => updateQuantity(item.id, item.quantity - 1)}
                  className="w-7 h-7 rounded-lg bg-orange-100 text-orange-600 flex items-center justify-center hover:bg-orange-200 transition-colors">
                  <Minus className="w-3 h-3" />
                </button>
                <span className="w-6 text-center font-bold text-gray-800">{item.quantity}</span>
                <button onClick={() => updateQuantity(item.id, item.quantity + 1)}
                  className="w-7 h-7 rounded-lg bg-orange-500 text-white flex items-center justify-center hover:bg-orange-600 transition-colors">
                  <Plus className="w-3 h-3" />
                </button>
              </div>
              <div className="text-right shrink-0 ml-2">
                <p className="font-bold text-gray-900">₹{(item.product.price * item.quantity).toFixed(0)}</p>
                <button onClick={() => removeItem(item.id)} className="text-red-400 hover:text-red-600 mt-1">
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))}
        </div>

        {/* Summary */}
        <div className="card p-5 h-fit sticky top-20">
          <h2 className="font-bold text-gray-800 text-lg mb-4" style={{ fontFamily: 'Plus Jakarta Sans' }}>Order Summary</h2>
          <div className="space-y-3 text-sm">
            <div className="flex justify-between text-gray-600">
              <span>Subtotal ({cart.total_items} items)</span>
              <span className="font-semibold">₹{cart.subtotal.toFixed(0)}</span>
            </div>
            <div className="flex justify-between text-gray-600">
              <span>Delivery fee</span>
              {cart.delivery_fee === 0
                ? <span className="text-green-600 font-semibold">FREE</span>
                : <span className="font-semibold">₹{cart.delivery_fee}</span>}
            </div>
            {cart.delivery_fee === 0 && (
              <p className="text-xs text-green-600 bg-green-50 rounded-lg px-3 py-2">🎉 You qualify for free delivery!</p>
            )}
            {cart.delivery_fee > 0 && (
              <p className="text-xs text-gray-500 bg-gray-50 rounded-lg px-3 py-2">
                Add ₹{(200 - cart.subtotal).toFixed(0)} more for free delivery
              </p>
            )}
            <div className="border-t pt-3 flex justify-between font-bold text-gray-900 text-base">
              <span>Total</span>
              <span>₹{cart.total.toFixed(0)}</span>
            </div>
          </div>
          <button onClick={() => navigate('/checkout')}
            className="w-full btn-primary mt-5 flex items-center justify-center gap-2">
            Proceed to Checkout <ArrowRight className="w-4 h-4" />
          </button>
          <Link to="/products" className="block text-center text-sm text-orange-500 font-semibold mt-3 hover:underline">
            + Add more items
          </Link>
        </div>
      </div>
    </div>
  )
}
