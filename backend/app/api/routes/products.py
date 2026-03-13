from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.db.database import get_db
from app.models.models import Product
from app.schemas.schemas import ProductWithCategory

router = APIRouter()


@router.get("/", response_model=List[ProductWithCategory])
def get_products(
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    in_stock: Optional[bool] = None,
    skip: int = 0,
    limit: int = Query(default=50, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Product).options(joinedload(Product.category))
    if category_id:
        query = query.filter(Product.category_id == category_id)
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    if in_stock is not None:
        query = query.filter(Product.in_stock == in_stock)
    return query.offset(skip).limit(limit).all()


@router.get("/{product_id}", response_model=ProductWithCategory)
def get_product(product_id: int, db: Session = Depends(get_db)):
    from fastapi import HTTPException
    product = db.query(Product).options(joinedload(Product.category)).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
