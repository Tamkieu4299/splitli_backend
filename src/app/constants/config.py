from functools import lru_cache

from psql import PSQLFactory
from pydantic import BaseSettings


@lru_cache()
def get_settings():
    return Settings()


class Settings(BaseSettings):
    """Config class read from .env"""

    API_VERSION: str
    DATABASE_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_HOSTNAME: str
    AWS_S3_URL: str
    AWS_S3_URL_GET: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    IMAGE_BUCKET: str
    DEFAULT_REGION: str

    @property
    def psql_factory(self) -> PSQLFactory:
        return PSQLFactory(
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOSTNAME}:{self.DATABASE_PORT}/{self.POSTGRES_DB}"
        )
    
    @property
    def fg_search_url(self) -> str:
        return f"http://{self.FG_SEARCH_DOMAIN}:{self.FG_SEARCH_PORT}/{self.API_VERSION}"


if __name__ == "__main__":
    settings = get_settings()
    factory = settings.psql_factory
    print(factory.__dict__)
