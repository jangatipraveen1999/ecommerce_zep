import { useQuery } from '@tanstack/react-query'
import { Clock, Package, CheckCircle, Truck } from 'lucide-react'
import api from '../utils/api'

const STATUS = {
  placed: { label: 'Order Placed', color: 'text-blue-600 bg-blue-50', icon: Package },
  confirmed: { label: 'Confirmed', color: 'text-orange-600 bg-orange-50', icon: CheckCircle },
  out_for_delivery: { label: 'Out for Delivery', color: 'text-purple-600 bg-purple-50', icon: Truck },
  delivered: { label: 'Delivered', color: 'text-green-600 bg-green-50', icon: CheckCircle },
}

export default function Orders() {
  const { data: orders = [], isLoading } = useQuery({
    queryKey: ['orders'],
    queryFn: () => api.get('/orders/').then(r => r.data)
  })

  if (isLoading) return <div className="flex items-center justify-center h-64"><div className="animate-spin w-8 h-8 border-4 border-orange-500 border-t-transparent rounded-full" /></div>

  if (orders.length === 0) {
    return (
      <div className="max-w-md mx-auto text-center py-20 px-4">
        <div className="text-8xl mb-6">📦</div>
        <h2 className="text-2xl font-bold text-gray-800 mb-2">No orders yet</h2>
        <p className="text-gray-500">Place your first order and track it here!</p>
      </div>
    )
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-6">
      <h1 className="text-2xl font-bold text-gray-900 mb-6" style={{ fontFamily: 'Plus Jakarta Sans' }}>My Orders</h1>
      <div className="space-y-4">
        {orders.map(order => {
          const status = STATUS[order.status] || STATUS.placed
          const StatusIcon = status.icon
          return (
            <div key={order.id} className="card p-5">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <p className="font-bold text-gray-800">Order #{order.id}</p>
                  <p className="text-xs text-gray-400 flex items-center gap-1 mt-0.5">
                    <Clock className="w-3 h-3" />
                    {new Date(order.created_at).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })}
                  </p>
                </div>
                <span className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-bold ${status.color}`}>
                  <StatusIcon className="w-3 h-3" /> {status.label}
                </span>
              </div>

              <div className="space-y-2 mb-4">
                {order.items.map(item => (
                  <div key={item.id} className="flex items-center gap-3">
                    <img src={item.product.image_url} alt={item.product.name}
                      className="w-10 h-10 rounded-lg object-cover bg-gray-50"
                      onError={e => e.target.src = 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=100'} />
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-700 truncate">{item.product.name}</p>
                      <p className="text-xs text-gray-400">× {item.quantity}</p>
                    </div>
                    <p className="text-sm font-semibold text-gray-800">₹{(item.price * item.quantity).toFixed(0)}</p>
                  </div>
                ))}
              </div>

              <div className="border-t pt-3 flex items-center justify-between text-sm">
                <div>
                  <p className="text-gray-500">Delivery to</p>
                  <p className="text-gray-700 font-medium text-xs truncate max-w-xs">{order.delivery_address}</p>
                </div>
                <div className="text-right">
                  <p className="text-gray-500">Total paid</p>
                  <p className="font-bold text-gray-900">₹{order.total_amount.toFixed(0)}</p>
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
