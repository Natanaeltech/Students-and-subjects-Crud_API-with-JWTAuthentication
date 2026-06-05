import os
from datetime import timedelta

class Settings:
    PROJECT_NAME: str = "Book CRUD API"
    VERSION: str = "1.0.0"
    
    # MySQL URL format: mysql+pymysql://user:password@host:port/database
    DB_USER: str = os.getenv("DB_USER", "root")          # votre utilisateur MySQL
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")      # votre mot de passe
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "3306")
    DB_NAME: str = os.getenv("DB_NAME", "bookdb")        # nom de la base à créer
    
    DATABASE_URL: str = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", ";MQg,r+.nXt8rJLc5Jx(J&T{u@OX^+qS")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    BCRYPT_ROUNDS: int = 12

settings = Settings()