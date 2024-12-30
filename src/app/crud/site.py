from models.site import Site
from ._base_crud import CRUDBase
from typing import List, Optional
from sqlalchemy.orm import Session

class CRUDSite(CRUDBase[Site]):
    def filter_sites(
        self,
        db: Session,
        name: Optional[str] = None,
        city: Optional[str] = None,
        street: Optional[str] = None,
        amount_of_donors: Optional[int] = None,
        amount_of_blood: Optional[int] = None,
        skip: int = 0,
        limit: int = 10,
    ):
        query = db.query(self.model)
        
        if name:
            query = query.filter(self.model.name.ilike(f"%{name}%"))
        if city:
            query = query.filter(self.model.city.ilike(f"%{city}%"))
        if street:
            query = query.filter(self.model.street.ilike(f"%{street}%"))
        if amount_of_donors is not None:
            query = query.filter(self.model.amount_of_donors >= amount_of_donors)
        if amount_of_blood is not None:
            query = query.filter(self.model.amount_of_blood >= amount_of_blood)
        
        total = query.count()
        results = query.all()
        return {"total": total, "results": results}