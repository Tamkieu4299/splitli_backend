from datetime import timedelta

from constants.config import Settings, get_settings
from crud.group import CRUD
from db.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from secret import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    TOKEN_TYPE,
    authenticate_user,
    create_access_token,
)
from sqlalchemy.orm import Session
from utils.common import serialize_model
from utils.exception import InvalidDestination
from utils.logger import setup_logger
from schemas.group import GroupAdd
from models.group import Group
from app.utils.response import Response

logger = setup_logger(__name__)

router = APIRouter()

group_crud = CRUD(Group)

@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED
)
async def create(
    payload: GroupAdd,
    db: Session = Depends(get_db),
):
    group = await group_crud.create(payload.dict(), db)
    if group is None:
        logger.info(f"Fail to create group")
        raise InvalidDestination(message=f"Fail to create group")
    return Response(content=group.__dict__)