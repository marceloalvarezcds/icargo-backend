from decouple import config as environ  # type: ignore

dburl = str(environ("DATABASE_URL", "localhost:5432"))
dbuser = str(environ("DATABASE_USER", "test"))
dbpasw = str(environ("DATABASE_PASS", "test"))
dbname = str(environ("DATABASE_NAME", "test"))
dbtype = str(environ("DATABASE_TYPE", "postgresql"))

# 60 minutes * 24 hours * 8 days = 8 days
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

API_BASE_URL = ""

JWT_ALGORITHM = "HS256"

SECRET_KEY = str(environ("SECRET_KEY", "secret_key"))

SQLALCHEMY_DATABASE_URI = f"{dbtype}://{dbuser}:{dbpasw}@{dburl}/{dbname}"
