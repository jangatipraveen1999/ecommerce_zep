import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Zap } from 'lucide-react'
import useAuthStore from '../store/authStore'
import toast from 'react-hot-toast'

export default function Register() {
  const [form, setForm] = useState({ name: '', email: '', phone: '', password: '', address: '' })
  const [loading, setLoading] = useState(false)
  const { register } = useAuthStore()
  const navigate = useNavigate()

  const update = (k, v) => setForm(f => ({ ...f, [k]: v }))

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      await register(form)
      toast.success('Account created! Welcome to ZapKart 🎉')
      navigate('/')
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Registration failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-amber-50 flex items-center justify-center px-4 py-8">
      <div className="bg-white rounded-3xl shadow-xl w-full max-w-md p-8">
        <div className="text-center mb-8">
          <Link to="/" className="inline-flex items-center gap-2 mb-6">
            <div className="w-10 h-10 bg-orange-500 rounded-xl flex items-center justify-center">
              <Zap className="w-6 h-6 text-white fill-white" />
            </div>
            <span className="text-2xl font-extrabold" style={{ fontFamily: 'Plus Jakarta Sans' }}>
              Zap<span className="text-orange-500">Kart</span>
            </span>
          </Link>
          <h1 className="text-2xl font-bold text-gray-900" style={{ fontFamily: 'Plus Jakarta Sans' }}>Create account</h1>
          <p className="text-gray-500 mt-1">Get groceries delivered in 10 minutes</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          {[
            { key: 'name', label: 'Full Name', type: 'text', placeholder: 'Praveen Kumar', required: true },
            { key: 'email', label: 'Email', type: 'email', placeholder: 'you@example.com', required: true },
            { key: 'phone', label: 'Phone', type: 'tel', placeholder: '+91 99999 99999', required: false },
            { key: 'password', label: 'Password', type: 'password', placeholder: 'Min. 8 characters', required: true },
            { key: 'address', label: 'Delivery Address', type: 'text', placeholder: 'Your full address', required: false },
          ].map(({ key, label, type, placeholder, required }) => (
            <div key={key}>
              <label className="block text-sm font-semibold text-gray-700 mb-1.5">{label} {required && <span className="text-red-400">*</span>}</label>
              <input value={form[key]} onChange={e => update(key, e.target.value)} type={type} placeholder={placeholder} required={required}
                className="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-orange-400" />
            </div>
          ))}
          <button type="submit" disabled={loading} className="w-full btn-primary flex items-center justify-center gap-2 disabled:opacity-60 mt-2">
            {loading ? <><span className="animate-spin w-4 h-4 border-2 border-white border-t-transparent rounded-full" /> Creating account...</> : 'Create Account'}
          </button>
        </form>

        <p className="text-center text-sm text-gray-500 mt-6">
          Already have an account? <Link to="/login" className="text-orange-500 font-semibold hover:underline">Sign in</Link>
        </p>
      </div>
    </div>
  )
}
