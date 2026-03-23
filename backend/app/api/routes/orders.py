from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.db.database import get_db
from app.models.models import Order, OrderItem, CartItem, User
from app.schemas.schemas import OrderCreate, OrderOut
from app.utils.deps import get_current_user

router = APIRouter()


@router.post("/place", response_model=OrderOut, status_code=201)
def place_order(order_data: OrderCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cart_items = db.query(CartItem).options(joinedload(CartItem.product)).filter(CartItem.user_id == current_user.id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    subtotal = sum(item.product.price * item.quantity for item in cart_items)
    delivery_fee = 0 if subtotal >= 200 else 20
    total = subtotal + delivery_fee
    order = Order(
        user_id=current_user.id,
        status="placed",
        total_amount=total,
        delivery_address=order_data.delivery_address,
        payment_method=order_data.payment_method,
        delivery_time=10,
    )
    db.add(order)
    db.flush()
    for item in cart_items:
        db.add(OrderItem(order_id=order.id, product_id=item.product_id, quantity=item.quantity, price=item.product.price))
    db.query(CartItem).filter(CartItem.user_id == current_user.id).delete()
    db.commit()
    db.refresh(order)
    return db.query(Order).options(joinedload(Order.items).joinedload(OrderItem.product)).filter(Order.id == order.id).first()


@router.get("/", response_model=List[OrderOut])
def get_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Order).options(joinedload(Order.items).joinedload(OrderItem.product)).filter(Order.user_id == current_user.id).order_by(Order.created_at.desc()).all()


@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = db.query(Order).options(joinedload(Order.items).joinedload(OrderItem.product)).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
