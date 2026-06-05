from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from database import get_session
from src.schemas.user import UserCreate, UserRead
from src.schemas.token import Token
from src.services.user_service import UserService
from src.services.auth_service import AuthService
from src.dependencies.auth import get_current_user, oauth2_scheme
from src.Models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserRead)
def register(user_create: UserCreate, session: Session = Depends(get_session)):
    return UserService.create_user(session, user_create)

@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = UserService.get_by_email(session, form_data.username)
    if not user or not AuthService.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = AuthService.create_access_token(user.id)
    return Token(access_token=access_token)

@router.get("/me", response_model=UserRead)
def me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/logout")
def logout(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    AuthService.blacklist_token(token, session)
    return {"message": "Successfully logged out"}

@router.post("/refresh", response_model=Token)
def refresh(current_user: User = Depends(get_current_user)):
    new_token = AuthService.create_access_token(current_user.id)
    return Token(access_token=new_token)