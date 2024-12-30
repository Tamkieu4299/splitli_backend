import logging

from crud._base_crud import CRUDBase
from models.donation import Donation
from sqlalchemy.orm import Session, joinedload
from utils.exception import NotFoundException

logger = logging.getLogger(__name__)

class CRUDDonation(CRUDBase[Donation]):
    def get_applications_by_job(
        self, site_id: int, db: Session
    ):
        donation = (
            db.query(Donation)
            .options(joinedload(Donation.user))
            .filter(Donation.site_id == site_id)
            .all()
        )
        return [ji.__dict__ for ji in donation]
    
    def read_by_user_id_and_donation_id(
        self, user_id: int, site_id: int, db: Session
    ):
        donation = (
            db.query(Donation)
            .filter(Donation.site_id == site_id, Donation.user_id == user_id)
            .first()
        )
        if not donation:
            return None
        return donation.__dict__
    
    def get_donation_by_id(
            self, id: int, db: Session
    ):
        donation = (
            db.query(Donation)
            .filter(Donation.id == id)
            .first()
        )

        if not donation:
            return None
        
        return donation

    def get_by_site_id(self, site_id: int, db: Session):
        try:
            result = db.query(Donation).filter(Donation.site_id == site_id).all()
            return result
        except Exception as e:
            logger.error(f"Error fetching: {e}", exc_info=True)
            raise e
        
    def get_by_site_id_and_user_id(self, site_id: int, user_id: int, db: Session):
        try:
            result = db.query(Donation).filter(Donation.site_id == site_id, Donation.user_id == user_id).first()
            return result
        except Exception as e:
            logger.error(f"Error fetching: {e}", exc_info=True)
            raise e

    def get_all(self, db: Session):
        try:
            result = db.query(Donation).all()
            return result
        except Exception as e:
            logger.error(f"Error fetching: {e}", exc_info=True)
            raise e

    