import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { MapPin, CreditCard, Truck, CheckCircle } from 'lucide-react'
import api from '../utils/api'
import useCartStore from '../store/cartStore'
import useAuthStore from '../store/authStore'
import toast from 'react-hot-toast'

export default function Checkout() {
  const { cart, fetchCart } = useCartStore()
  const { user } = useAuthStore()
  const navigate = useNavigate()
  const [address, setAddress] = useState(user?.address || '')
  const [payment, setPayment] = useState('cod')
  const [placing, setPlacing] = useState(false)
  const [success, setSuccess] = useState(false)

  if (!cart || cart.items.length === 0) {
    navigate('/cart'); return null
  }

  const placeOrder = async () => {
    if (!address.trim()) { toast.error('Please enter delivery address'); return }
    setPlacing(true)
    try {
      await api.post('/orders/place', { delivery_address: address, payment_method: payment })
      setSuccess(true)
      await fetchCart()
    } catch {
      toast.error('Failed to place order. Try again.')
    } finally {
      setPlacing(false)
    }
  }

  if (success) {
    return (
      <div className="max-w-md mx-auto text-center py-20 px-4">
        <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
          <CheckCircle className="w-12 h-12 text-green-500" />
        </div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Order Placed! 🎉</h2>
        <p className="text-gray-500 mb-2">Your groceries will arrive in <span className="font-bold text-purple-600">10 minutes</span></p>
        <p className="text-sm text-gray-400 mb-8">Delivering to: {address}</p>
        <div className="flex flex-col gap-3">
          <button onClick={() => navigate('/orders')} className="btn-primary">Track Order</button>
          <button onClick={() => navigate('/')} className="btn-secondary">Continue Shopping</button>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-5xl mx-auto px-4 py-6">
      <h1 className="text-2xl font-bold text-gray-900 mb-6" style={{ fontFamily: 'Plus Jakarta Sans' }}>Checkout</h1>
      <div className="grid md:grid-cols-[1fr_360px] gap-6">
        <div className="space-y-4">
          {/* Address */}
          <div className="card p-5">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
                <MapPin className="w-4 h-4 text-orange-600" />
              </div>
              <h2 className="font-bold text-gray-800">Delivery Address</h2>
            </div>
            <textarea value={address} onChange={e => setAddress(e.target.value)} rows={3}
              placeholder="Enter your full delivery address..."
              className="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-orange-400 resize-none"
            />
          </div>

          {/* Payment */}
          <div className="card p-5">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
                <CreditCard className="w-4 h-4 text-orange-600" />
              </div>
              <h2 className="font-bold text-gray-800">Payment Method</h2>
            </div>
            <div className="space-y-2">
              {[
                { id: 'cod', label: 'Cash on Delivery', icon: '💵' },
                { id: 'upi', label: 'UPI / QR Code', icon: '📱' },
                { id: 'card', label: 'Credit / Debit Card', icon: '💳' },
              ].map(opt => (
                <label key={opt.id} className={`flex items-center gap-3 p-3 border-2 rounded-xl cursor-pointer transition-all ${payment === opt.id ? 'border-orange-400 bg-orange-50' : 'border-gray-100 hover:border-gray-200'}`}>
                  <input type="radio" name="payment" value={opt.id} checked={payment === opt.id} onChange={() => setPayment(opt.id)} className="text-orange-500" />
                  <span className="text-lg">{opt.icon}</span>
                  <span className="text-sm font-medium text-gray-700">{opt.label}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Delivery info */}
          <div className="flex items-center gap-3 bg-purple-50 border border-purple-100 rounded-2xl px-4 py-3">
            <Truck className="w-5 h-5 text-purple-600 shrink-0" />
            <p className="text-sm text-purple-800 font-semibold">Express delivery in 10 minutes to your doorstep 🚀</p>
          </div>
        </div>

        {/* Summary */}
        <div className="card p-5 h-fit sticky top-20">
          <h2 className="font-bold text-gray-800 text-lg mb-4">Order Summary</h2>
          <div className="space-y-2 max-h-48 overflow-y-auto mb-4">
            {cart.items.map(item => (
              <div key={item.id} className="flex justify-between text-sm">
                <span className="text-gray-600 truncate flex-1 mr-2">{item.product.name} × {item.quantity}</span>
                <span className="font-semibold text-gray-800 shrink-0">₹{(item.product.price * item.quantity).toFixed(0)}</span>
              </div>
            ))}
          </div>
          <div className="border-t pt-3 space-y-2 text-sm">
            <div className="flex justify-between text-gray-600"><span>Subtotal</span><span>₹{cart.subtotal.toFixed(0)}</span></div>
            <div className="flex justify-between text-gray-600"><span>Delivery</span><span className={cart.delivery_fee === 0 ? 'text-green-600 font-semibold' : ''}>{cart.delivery_fee === 0 ? 'FREE' : `₹${cart.delivery_fee}`}</span></div>
            <div className="border-t pt-2 flex justify-between font-bold text-base"><span>Total</span><span>₹{cart.total.toFixed(0)}</span></div>
          </div>
          <button onClick={placeOrder} disabled={placing}
            className="w-full btn-primary mt-5 flex items-center justify-center gap-2 disabled:opacity-60">
            {placing ? <><span className="animate-spin w-4 h-4 border-2 border-white border-t-transparent rounded-full" /> Placing Order...</> : <>Place Order • ₹{cart.total.toFixed(0)}</>}
          </button>
        </div>
      </div>
    </div>
  )
}
