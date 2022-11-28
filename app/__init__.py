from decouple import config as environ  # type: ignore
from fastapi import FastAPI

from app.logger import logger  # noqa

root_path = str(environ("API_ROOT_PATH", ""))

app = FastAPI(title="ICargo API", root_path=root_path)
