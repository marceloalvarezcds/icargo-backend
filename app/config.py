import os
from typing import List, Union

import jinja2
from decouple import config as environ  # type: ignore
from pydantic import AnyHttpUrl, BaseSettings, validator  # type: ignore

dir_path = os.path.dirname(os.path.realpath(__file__))
REPORTS_FOLDER_NAME = "reports"
REPORTS_FOLDER = os.path.join(dir_path, REPORTS_FOLDER_NAME)
STATICS_FOLDER_NAME = "statics"
STATICS_FOLDER = os.path.join(dir_path, STATICS_FOLDER_NAME)

TEMPLATES_FOLDER = os.path.join(dir_path, "templates")
templateLoader = jinja2.FileSystemLoader(searchpath=TEMPLATES_FOLDER)
templateEnv = jinja2.Environment(loader=templateLoader)

if not os.path.exists(REPORTS_FOLDER):
    os.mkdir(REPORTS_FOLDER)

dburl = str(environ("DATABASE_URL", "localhost:5432"))
dbuser = str(environ("DATABASE_USER", "test"))
dbpasw = str(environ("DATABASE_PASS", "test"))
dbname = str(environ("DATABASE_NAME", "test"))
dbtype = str(environ("DATABASE_TYPE", "postgresql"))
DATABASE_INITIALIZE_WITHOUT_SEEDS = (
    str(environ("DATABASE_INITIALIZE_WITHOUT_SEEDS", "false")) == "true"
)

# 60 minutes * 24 hours * 8 days = 8 days
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

API_BASE_URL = str(environ("API_BASE_URL", "http://localhost:8101"))

DECIMAL_PRECISION = int(str(environ("DECIMAL_PRECISION", "2")))

STATICS_URL = f"{API_BASE_URL}/{STATICS_FOLDER_NAME}"

LOGO_IMAGE_URL = f"{STATICS_URL}/logo-icargo.png"

ENV = str(environ("ENV", "development"))

JWT_ALGORITHM = "HS256"

SECRET_KEY = str(environ("SECRET_KEY", "secret_key"))

SQLALCHEMY_DATABASE_URI = f"{dbtype}://{dbuser}:{dbpasw}@{dburl}/{dbname}"

USER_ADMIN_PASS = str(environ("USER_ADMIN_PASS", "user_admin"))


PICTSHARE_API = str(environ("PICTSHARE_API", "http://localhost:8103/api"))


class PictShareSettings(BaseSettings):
    PICTSHARE_DOCKER: str = "http://pictshare/api"
    PICTSHARE_UPLOAD: str = "/upload.php"


class Settings(BaseSettings):
    BACKEND_CORS_ORIGINS: List[Union[str, AnyHttpUrl]] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)


settings = Settings()
