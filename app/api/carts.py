from fastapi import APIRouter, Depends, HTTPException
from app.schemas import CartCreate, CartRead, CartItemCreate, CartItemRead, CartItemUpdate
from sqlmodel import Session
from app.database import get_session
from app.services import cart_service


router = APIRouter()


@router.post("/carts", response_model=CartRead, status_code=201)
def create_cart(cart: CartCreate, session: Session = Depends(get_session)):
    return cart_service.create_cart(session=session, cart=cart)


@router.get("/carts/{cart_id}", response_model=CartRead)
def get_cart(cart_id: int, session: Session = Depends(get_session)):
    cart = cart_service.get_cart(session, cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart


@router.post("/carts/{cart_id}/items", response_model=CartItemRead, status_code=201)
def add_item(cart_id: int, item: CartItemCreate, session: Session = Depends(get_session)):
    db_item = cart_service.add_item(session=session, cart_id=cart_id, item=item)
    if not db_item:
        raise HTTPException(status_code=404, detail="Cart not found")
    return db_item


@router.put("/carts/items/{item_id}", response_model=CartItemRead)
def update_item(item_id: int, item: CartItemUpdate, session: Session = Depends(get_session)):
    db_item = cart_service.update_item(session=session, item_id=item_id, item=item)
    if not db_item:
        raise HTTPException(status_code=404, detail="Cart Item not found")
    return db_item
    
@router.delete("/carts/items/{item_id}", status_code=204)
def remove_item(item_id: int, session: Session = Depends(get_session)):
    removed = cart_service.remove_item(session=session, item_id=item_id)
    if not removed:
        raise HTTPException(status_code=404, detail="Cart Item not found")
    
      