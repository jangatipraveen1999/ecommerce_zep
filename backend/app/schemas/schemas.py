from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# Auth Schemas
class UserCreate(BaseModel):
    email: EmailStr
    name: str
    phone: Optional[str] = None
    password: str
    address: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: str
    name: str
    phone: Optional[str]
    address: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserOut


# Category Schemas
class CategoryOut(BaseModel):
    id: int
    name: str
    icon: Optional[str]
    slug: str
    color: str

    class Config:
        from_attributes = True


# Product Schemas
class ProductOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    original_price: Optional[float]
    unit: Optional[str]
    image_url: Optional[str]
    category_id: int
    discount: int
    in_stock: bool
    delivery_time: int
    rating: float
    review_count: int

    class Config:
        from_attributes = True


class ProductWithCategory(ProductOut):
    category: Optional[CategoryOut]


# Cart Schemas
class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 1


class CartItemUpdate(BaseModel):
    quantity: int


class CartItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    product: ProductOut

    class Config:
        from_attributes = True


class CartOut(BaseModel):
    items: List[CartItemOut]
    total_items: int
    subtotal: float
    delivery_fee: float
    total: float


# Order Schemas
class OrderCreate(BaseModel):
    delivery_address: str
    payment_method: str = "cod"


class OrderItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: float
    product: ProductOut

    class Config:
        from_attributes = True


class OrderOut(BaseModel):
    id: int
    status: str
    total_amount: float
    delivery_address: str
    delivery_time: int
    payment_method: str
    created_at: datetime
    items: List[OrderItemOut]

    class Config:
        from_attributes = True
