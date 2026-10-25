from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from app.schemas import OrderRead
from app.database import get_session
from app.services import order_service

router = APIRouter()


@router.post("/checkout/{cart_id}", response_model=OrderRead, status_code=201)
def checkout(cart_id: int, session: Session = Depends(get_session)):
    try:
        return order_service.checkout(session, cart_id)
    except ValueError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/orders/{order_id}", response_model=OrderRead)
def get_order(order_id: int, session: Session = Depends(get_session)):
    order = order_service.get_order(session, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order