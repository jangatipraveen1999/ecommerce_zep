# ⚡ ZapKart — Zepto-inspired Quick Commerce App

> Groceries delivered in **10 minutes** | Built with **FastAPI** + **React**

---

## 🏗️ Project Structure

```
zapkart/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── main.py             # FastAPI entry point
│   │   ├── api/
│   │   │   └── routes/         # Route handlers
│   │   │       ├── auth.py
│   │   │       ├── products.py
│   │   │       ├── categories.py
│   │   │       ├── cart.py
│   │   │       └── orders.py
│   │   ├── core/
│   │   │   ├── config.py       # App settings
│   │   │   └── security.py     # JWT & password hashing
│   │   ├── db/
│   │   │   ├── database.py     # SQLAlchemy setup
│   │   │   └── seed.py         # Demo data seeder
│   │   ├── models/
│   │   │   └── models.py       # SQLAlchemy ORM models
│   │   ├── schemas/
│   │   │   └── schemas.py      # Pydantic schemas
│   │   └── utils/
│   │       └── deps.py         # Auth dependencies
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/                   # React + Vite Frontend
│   ├── src/
│   │   ├── main.jsx            # App entry point
│   │   ├── App.jsx             # Router setup
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   │   ├── Layout.jsx  # Page shell
│   │   │   │   └── Navbar.jsx  # Top navigation
│   │   │   └── product/
│   │   │       └── ProductCard.jsx
│   │   ├── pages/
│   │   │   ├── Home.jsx        # Landing + hero
│   │   │   ├── Products.jsx    # Browse + filter
│   │   │   ├── Cart.jsx        # Shopping cart
│   │   │   ├── Checkout.jsx    # Place order
│   │   │   ├── Orders.jsx      # Order history
│   │   │   ├── Login.jsx
│   │   │   └── Register.jsx
│   │   ├── store/
│   │   │   ├── authStore.js    # Zustand auth state
│   │   │   └── cartStore.js    # Zustand cart state
│   │   ├── utils/
│   │   │   └── api.js          # Axios instance
│   │   └── styles/
│   │       └── index.css
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── Dockerfile
│
├── docker-compose.yml
└── README.md
```

---

## 🚀 Local Setup Guide

### Prerequisites

Make sure you have these installed:
- **Python 3.10+** → [python.org](https://python.org)
- **Node.js 18+** → [nodejs.org](https://nodejs.org)
- **pip** (comes with Python)
- **Git** (optional, for cloning)

---

## Option A: Manual Setup (Recommended for Development)

### Step 1 — Backend Setup

```bash
# Navigate to backend folder
cd zapkart/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Seed the database with demo data
python -m app.db.seed

# Start the FastAPI server
uvicorn app.main:app --reload --port 8000
```

✅ Backend is running at: **http://localhost:8000**
📖 API Docs available at: **http://localhost:8000/api/docs**

---

### Step 2 — Frontend Setup

Open a **new terminal window**:

```bash
# Navigate to frontend folder
cd zapkart/frontend

# Install Node dependencies
npm install

# Start the React dev server
npm run dev
```

✅ Frontend is running at: **http://localhost:3000**

---

### Step 3 — Test the App

Open your browser at **http://localhost:3000**

**Demo Login:**
- Email: `demo@zapkart.com`
- Password: `demo123`

Or register a new account!

---

## Option B: Docker Setup (One Command)

### Prerequisites
- **Docker Desktop** → [docker.com](https://www.docker.com/products/docker-desktop/)

```bash
# From the zapkart/ root folder
cd zapkart

# Build and start everything
docker-compose up --build

# To stop:
docker-compose down
```

✅ Frontend: **http://localhost:3000**
✅ Backend: **http://localhost:8000/api/docs**

---

## 🔑 API Endpoints Reference

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login & get JWT token |

### Products
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/products/` | List products (with filters) |
| GET | `/api/products/?search=tomato` | Search products |
| GET | `/api/products/?category_id=1` | Filter by category |
| GET | `/api/products/{id}` | Get single product |

### Categories
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/categories/` | List all categories |

### Cart (requires JWT)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/cart/` | Get cart with totals |
| POST | `/api/cart/add` | Add item to cart |
| PUT | `/api/cart/{id}` | Update item quantity |
| DELETE | `/api/cart/{id}` | Remove item |
| DELETE | `/api/cart/` | Clear entire cart |

### Orders (requires JWT)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/orders/place` | Place order from cart |
| GET | `/api/orders/` | Get order history |
| GET | `/api/orders/{id}` | Get single order |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 18, Vite, Tailwind CSS |
| **State Management** | Zustand, TanStack Query |
| **Backend** | FastAPI, Python 3.11 |
| **Database** | SQLite (dev) / PostgreSQL (prod) |
| **ORM** | SQLAlchemy 2.0 |
| **Auth** | JWT (python-jose) + bcrypt |
| **Validation** | Pydantic v2 |
| **HTTP Client** | Axios |
| **Containerization** | Docker, Docker Compose |

---

## 🔧 Switching to PostgreSQL (Production)

1. Update `.env`:
```
DATABASE_URL=postgresql://user:password@localhost:5432/zapkart
```

2. Add psycopg2 to requirements:
```
psycopg2-binary==2.9.9
```

3. Re-run seed: `python -m app.db.seed`

---

## 💡 Common Issues

**Port already in use?**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

**Module not found errors?**
```bash
# Make sure venv is activated
source venv/bin/activate  # macOS/Linux
# Then reinstall
pip install -r requirements.txt
```

**CORS errors?**
- Make sure backend is running on port 8000
- Vite proxy is configured in `vite.config.js` to forward `/api` calls

---

## 📦 Features

- ✅ User registration & login with JWT
- ✅ Browse products by category
- ✅ Search products
- ✅ Add to cart / update quantities
- ✅ Free delivery threshold (₹200+)
- ✅ Checkout with address & payment method
- ✅ Order history tracking
- ✅ Responsive mobile-first design
- ✅ Swagger API documentation
- ✅ Demo data seeder

---

*Built with ❤️ for ZapKart — Interview-ready production code*
