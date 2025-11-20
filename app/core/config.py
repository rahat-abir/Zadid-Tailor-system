import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Tailor Management API (Inventory)"
    DB_USER: str = os.getenv("MYSQL_USER", "tailor")
    DB_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "tailorpass")
    DB_NAME: str = os.getenv("MYSQL_DATABASE", "tailor_db")
    DB_HOST: str = os.getenv("MYSQL_HOST", "db")
    DB_PORT: str = os.getenv("MYSQL_PORT", "3306")

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        # Using PyMySQL driver
        return (
            f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

settings = Settings()
