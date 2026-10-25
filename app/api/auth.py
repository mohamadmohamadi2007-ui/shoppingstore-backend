from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session

from app.config import settings
from app.database import get_session
from app.dependencies import get_current_customer
from app.schemas import Customer, CustomerRead
from app.security import create_access_token
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


class OTPRequest(BaseModel):
    phone_number: str


class OTPVerify(BaseModel):
    phone_number: str
    otp_code: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/otp/request")
def request_otp(payload: OTPRequest, session: Session = Depends(get_session)):
    _, otp_code = auth_service.request_otp(session, payload.phone_number)
    response = {"message": "OTP sent"}
    if settings.environment != "production":
        # No SMS gateway wired up yet (step 25 territory) — echo the code back
        # so the dev-phase flow is testable without any delivery cost.
        # This field must be removed before any production deploy.
        response["debug_otp"] = otp_code
    return response


@router.post("/otp/verify", response_model=TokenResponse)
def verify_otp(payload: OTPVerify, session: Session = Depends(get_session)):
    try:
        customer = auth_service.verify_otp(session, payload.phone_number, payload.otp_code)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return TokenResponse(access_token=create_access_token(customer.id))


@router.get("/me", response_model=CustomerRead)
def get_me(customer: Customer = Depends(get_current_customer)):
    return customer
