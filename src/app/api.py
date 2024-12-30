import os

from constants.config import Settings
from db.database import PSQLManager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from middleware.request_context import RequestContextMiddleware
from middleware.request_logging import RequestLoggingMiddleware
from models._base_model import _metadata_obj
from routers.auth import router as auth_router
from routers.site import router as site_router
from routers.donation import router as donation_router
from routers.map import router as map_router

settings = Settings()
PREFIX = f"/api/{settings.API_VERSION}"
_metadata_obj.create_all(bind=PSQLManager.Instance().get_base_engin(), checkfirst=True)

app = FastAPI(
    openapi_url=f"{PREFIX}/openapi.json",
    docs_url=f"{PREFIX}/docs",
    redoc_url=f"{PREFIX}/redoc",
)
app.mount(
    "/static",
    StaticFiles(
        directory=os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        + "/static",
        html=False,
    ),
    name="static",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RequestContextMiddleware)
app.add_middleware(RequestLoggingMiddleware)

# Include the router
app.include_router(auth_router, tags=["Authenication"], prefix=f"{PREFIX}/auth")
app.include_router(site_router, tags=["Site"], prefix=f"{PREFIX}/site")
app.include_router(donation_router, tags=["Donation"], prefix=f"{PREFIX}/donation")
app.include_router(map_router, tags=["Map"], prefix=f"{PREFIX}/map")





