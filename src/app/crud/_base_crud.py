from typing import Generic, TypeVar
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
import logging

ModelType = TypeVar("ModelType", bound=DeclarativeMeta)
logger = logging.getLogger(__name__)

class CRUDBase(Generic[ModelType]):
    def __init__(self, model: ModelType):
        self.model = model

    async def create(self, obj_in: dict, db: Session):
        try:
            db_obj = self.model(**obj_in)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            logger.error(f"Error creating object: {e}", exc_info=True)
            db.rollback()
            raise e

    def read(self, id: int, db: Session):
        try:
            return db.query(self.model).filter(self.model.id == id).first()
        except Exception as e:
            logger.error(f"Error reading object with ID {id}: {e}", exc_info=True)
            raise e

    def update(self, id: int, obj_in: dict, db: Session):
        try:
            db_obj = db.query(self.model).filter(self.model.id == id).first()
            if not db_obj:
                logger.error(f"Object with ID {id} not found for update.")
                return None
            for key, value in obj_in.items():
                if value is not None:
                    setattr(db_obj, key, value)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            logger.error(f"Error updating object with ID {id}: {e}", exc_info=True)
            db.rollback()
            raise e

    def _upsert(self, model_class, data, db: Session):
        try:
            if "id" in data:
                instance = db.query(model_class).filter_by(id=data["id"]).first()
                if instance:
                    for key, value in data.items():
                        setattr(instance, key, value)
                else:
                    instance = model_class(**data)
                    db.add(instance)
            else:
                instance = model_class(**data)
                db.add(instance)
            return instance
        except Exception as e:
            logger.error(f"Error in upsert operation: {e}", exc_info=True)
            db.rollback()
            raise e

    def _upsert_many(self, model_class, data_list, db: Session):
        try:
            instances = [self._upsert(model_class, data, db) for data in data_list]
            db.commit()
            return instances
        except Exception as e:
            logger.error(f"Error in upsert many operation: {e}", exc_info=True)
            db.rollback()
            raise e

    def soft_delete(self, id: int, db: Session):
        try:
            db_obj = db.query(self.model).filter(self.model.id == id).first()
            if not db_obj:
                logger.error(f"Object with ID {id} not found for soft delete.")
                return None
            db_obj.is_deleted = True
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            logger.error(f"Error in soft deleting object with ID {id}: {e}", exc_info=True)
            db.rollback()
            raise e

    def delete(self, id: int, db: Session):
        try:
            db_obj = db.query(self.model).filter(self.model.id == id).first()
            if not db_obj:
                logger.error(f"Object with ID {id} not found for deletion.")
                return None
            db.delete(db_obj)
            db.commit()
            return db_obj
        except Exception as e:
            logger.error(f"Error deleting object with ID {id}: {e}", exc_info=True)
            db.rollback()
            raise e

    def get_all(self, db: Session, order_by: str = None, order_direction: str = "asc", skip: int = 0, limit: int = 10,):
        try:
            query = db.query(self.model)
            
            # Apply ordering if order_by is provided
            if order_by:
                order_column = getattr(self.model, order_by, None)
                if not order_column:
                    raise ValueError(f"Invalid order_by column: {order_by}")
                
                if order_direction.lower() == "desc":
                    query = query.order_by(desc(order_column))
                else:
                    query = query.order_by(asc(order_column))
            
            # Apply skip and limit
            return query.all()
        except Exception as e:
            logger.error(f"Error fetching all objects: {e}", exc_info=True)
            raise e
