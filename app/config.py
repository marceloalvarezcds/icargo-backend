from pydantic import BaseSettings

class TokenSettings(BaseSettings):
    SECRET_KEY: str = "3dc9e33440d7bc87558b859b1133e456df4cfd6be9061bd147fa4bf8234c37ea"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
