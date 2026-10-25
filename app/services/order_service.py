from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from app.schemas import Order, OrderItem, Cart, CartItem, Variant, Product


def checkout(session: Session, cart_id: int):
    db_cart = session.get(Cart, cart_id)
    if not db_cart:
        raise ValueError("cart not found")

    query = select(CartItem).where(
        CartItem.cart_id == cart_id
    )
    db_cart_items = session.exec(query).all()
    if not db_cart_items:
        raise ValueError("cart is empty!")

    order = Order(
        customer_id= db_cart.customer_id,
        status= "pending",
        total= 0
        )
    session.add(order)

    total = 0
    for cart_item in db_cart_items:
        db_variant = session.get(Variant, cart_item.variant_id)
        if db_variant.stock_qty < cart_item.qty:
            raise ValueError(f"insufficient stock for variant {db_variant.id}")

        if db_variant.price_override is not None:
            price = db_variant.price_override
        else:
            db_product = session.get(Product, db_variant.product_id)
            price = db_product.base_price

        db_variant.stock_qty -= cart_item.qty
        session.add(db_variant)
        session.add(OrderItem(
            order= order,
            variant_id= db_variant.id,
            qty= cart_item.qty,
            price= price
        ))
        total += price * cart_item.qty
        session.delete(cart_item)

    order.total = total
    session.add(order)
    session.commit()
    session.refresh(order)
    return order

def get_order(session: Session, order_id: int):

    query = select(Order).where(
        Order.id == order_id
    ).options(
        selectinload(Order.items)
        .selectinload(OrderItem.variant)
    )
    return session.exec(query).first()


