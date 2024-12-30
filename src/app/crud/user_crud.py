from app.models.user import User
from sqlalchemy.orm import Session

from ._base_crud import CRUDBase


class CRUDUser(CRUDBase[User]):
    def search_user_by_phone_number(
        self, phone_numer: str, db: Session
    ) -> User:
        user = (
            db.query(User)
            .filter(User.phone == phone_numer and User.is_deleted == False)
            .first()
        )
        return user

    def search_user_by_email(self, email: str, db: Session) -> User:
        user = (
            db.query(User)
            .filter(User.email == email and User.is_deleted == False)
            .first()
        )
        return user

    def search_user(self, name: str, db: Session) -> User:
        user = (
            db.query(User)
            .filter(User.user_name == name and User.is_deleted == False)
            .first()
        )

        return user
