from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.db.database import get_db
from app.models.models import CartItem, Product, User
from app.schemas.schemas import CartItemCreate, CartItemUpdate, CartOut
from app.utils.deps import get_current_user

router = APIRouter()

DELIVERY_FEE = 20.0
FREE_DELIVERY_THRESHOLD = 200.0


def compute_cart(items):
    subtotal = sum(item.product.price * item.quantity for item in items)
    delivery_fee = 0.0 if subtotal >= FREE_DELIVERY_THRESHOLD else DELIVERY_FEE
    return {
        "items": items,
        "total_items": sum(item.quantity for item in items),
        "subtotal": subtotal,
        "delivery_fee": delivery_fee,
        "total": subtotal + delivery_fee,
    }


@router.get("/", response_model=CartOut)
def get_cart(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    items = db.query(CartItem).options(joinedload(CartItem.product)).filter(CartItem.user_id == current_user.id).all()
    return compute_cart(items)


@router.post("/add")
def add_to_cart(item: CartItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    existing = db.query(CartItem).filter(CartItem.user_id == current_user.id, CartItem.product_id == item.product_id).first()
    if existing:
        existing.quantity += item.quantity
    else:
        db.add(CartItem(user_id=current_user.id, product_id=item.product_id, quantity=item.quantity))
    db.commit()
    return {"message": "Added to cart"}


@router.put("/{item_id}")
def update_cart_item(item_id: int, update: CartItemUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cart_item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.user_id == current_user.id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    if update.quantity <= 0:
        db.delete(cart_item)
    else:
        cart_item.quantity = update.quantity
    db.commit()
    return {"message": "Cart updated"}


@router.delete("/{item_id}")
def remove_from_cart(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cart_item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.user_id == current_user.id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    db.delete(cart_item)
    db.commit()
    return {"message": "Item removed"}


@router.delete("/")
def clear_cart(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db.query(CartItem).filter(CartItem.user_id == current_user.id).delete()
    db.commit()
    return {"message": "Cart cleared"}
