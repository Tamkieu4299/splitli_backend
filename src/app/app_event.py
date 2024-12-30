
from api import app
from db.database import PSQLManager


@app.on_event("startup")
def startup_event():
    PSQLManager.Instance()


