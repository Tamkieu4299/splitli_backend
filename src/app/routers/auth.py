from datetime import timedelta

from constants.config import Settings, get_settings
from crud.user_crud import CRUDUser
from db.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.auth_schema import (
    LoginResponse,
    LoginSchema,
    RegisterResponse,
    UserRegisterBaseSchema
)
from schemas.response_schema import ResponseData
from secret import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    TOKEN_TYPE,
    authenticate_user,
    create_access_token,
)
from sqlalchemy.orm import Session
from utils.common import serialize_model
from utils.exception import InvalidDestination
from utils.hash import hash_password
from utils.logger import setup_logger

from app.models.user import User
from app.utils.response import Response

logger = setup_logger(__name__)

router = APIRouter()

user_crud = CRUDUser(User)

@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=RegisterResponse,
)
async def register_user(
    user_data: UserRegisterBaseSchema,
    db: Session = Depends(get_db),
):
    user = user_crud.search_user_by_email(user_data.email, db)
    if user:
        raise HTTPException(
            status_code=422, detail="This email is already registered."
        )

    hash_user_data = user_data.dict()
    hash_user_data["password"] = hash_password(hash_user_data["password"])

    new_user = await user_crud.create(hash_user_data, db)

    if new_user is None:
        logger.info(f"Fail to create user")
        raise InvalidDestination(message=f"Fail to create user")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(new_user.id)},
        expires_delta=access_token_expires,
    )
    new_user.token = access_token
    new_user.token_type = TOKEN_TYPE

    rsp = RegisterResponse.from_orm(new_user)

    return Response(content=rsp)


@router.post("/token", response_model=ResponseData)
def login_for_access_token(
    form_data: LoginSchema,
    settings: Settings = Depends(get_settings),
    db: Session = Depends(get_db),
):

    user = authenticate_user(db, form_data.email, form_data.password)

    if not user:
        logger.error(
            f"email={form_data.email} User authentication failed because the email or password is invalid."
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": TOKEN_TYPE},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "role": user.role,
        },
        expires_delta=access_token_expires,
    )

    logger.info(f"email={form_data.email} authentication succeeded")
    user.token = access_token
    user.token_type = TOKEN_TYPE

    response_data = LoginResponse.from_orm(user)

    return Response(content=response_data)
