from pathlib import Path
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    ES_URL: str
    ES_USERNAME: str
    ES_PASSWORD: str
    ES_CA_CERT: str

    class Config:
        env_file = BASE_DIR / ".env"

settings=Settings()