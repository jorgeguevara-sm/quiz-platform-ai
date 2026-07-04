import stripe
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.config import settings
from app.routers.tests import get_current_user_from_header

router = APIRouter(prefix="/billing", tags=["billing"])
stripe.api_key = settings.stripe_secret_key


@router.post("/checkout/subscription")
def create_subscription_checkout(user: models.User = Depends(get_current_user_from_header)):
    session = stripe.checkout.Session.create(
        mode="subscription",
        payment_method_types=["card"],
        line_items=[{"price": settings.stripe_price_subscription, "quantity": 1}],
        customer_email=user.email,
        success_url=f"{settings.frontend_url}/dashboard?checkout=success",
        cancel_url=f"{settings.frontend_url}/pricing?checkout=cancel",
        client_reference_id=user.id,
    )
    return {"checkout_url": session.url}


@router.post("/checkout/pay-per-use")
def create_pay_per_use_checkout(user: models.User = Depends(get_current_user_from_header)):
    session = stripe.checkout.Session.create(
        mode="payment",
        payment_method_types=["card"],
        line_items=[{"price_data": {"currency": "usd",
            "product_data": {"name": "Generacion de test individual"},
            "unit_amount": 200}, "quantity": 1}],
        customer_email=user.email,
        success_url=f"{settings.frontend_url}/dashboard?checkout=success",
        cancel_url=f"{settings.frontend_url}/dashboard?checkout=cancel",
        client_reference_id=user.id,
    )
    return {"checkout_url": session.url}


@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.stripe_webhook_secret)
    except Exception:
        raise HTTPException(status_code=400, detail="Webhook invalido")
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        user_id = session.get("client_reference_id")
        mode = session.get("mode")
        user = db.query(models.User).filter_by(id=user_id).first()
        if user:
            if mode == "subscription":
                user.plan = "subscription"
                sub = models.Subscription(user_id=user.id,
                    stripe_subscription_id=session.get("subscription"), status="active")
                db.add(sub)
            elif mode == "payment":
                user.plan = "pay_per_use"
            db.commit()
    if event["type"] == "customer.subscription.deleted":
        sub_id = event["data"]["object"]["id"]
        sub = db.query(models.Subscription).filter_by(stripe_subscription_id=sub_id).first()
        if sub:
            sub.status = "canceled"
            user = db.query(models.User).filter_by(id=sub.user_id).first()
            if user:
                user.plan = "free"
            db.commit()
    return {"status": "ok"}
