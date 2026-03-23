from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import products, cart, orders, auth, categories
from app.core.config import settings
from app.db.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ZapKart API",
    description="Zepto-inspired quick commerce grocery delivery platform",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(categories.router, prefix="/api/categories", tags=["Categories"])
app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(cart.router, prefix="/api/cart", tags=["Cart"])
app.include_router(orders.router, prefix="/api/orders", tags=["Orders"])


@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "ZapKart API"}
