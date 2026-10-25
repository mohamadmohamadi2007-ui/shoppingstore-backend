from sqlmodel import Session
from app.schemas import CartCreate, Cart, CartItemCreate, CartItem, CartItemUpdate


def create_cart(session: Session, cart: CartCreate):
    db_cart = Cart.model_validate(cart)
    session.add(db_cart)
    session.commit()
    session.refresh(db_cart)
    return db_cart

def get_cart(session: Session, cart_id: int):
    return session.get(Cart, cart_id) 

def add_item(session: Session, cart_id: int, item: CartItemCreate):
    db_cart = session.get(Cart, cart_id)
    if not db_cart:
        return None
    db_item = CartItem(cart_id= cart_id, variant_id=item.variant_id, qty= item.qty)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

def update_item(session: Session, item_id: int, item: CartItemUpdate):
    db_item = session.get(CartItem, item_id)
    if not db_item:
        return None
    db_item.qty = item.qty
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

def remove_item(session: Session, item_id: int) -> bool:
    db_item = session.get(CartItem, item_id)
    if not db_item:
        return False
    session.delete(db_item)
    session.commit()
    return True
