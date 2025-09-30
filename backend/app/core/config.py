import os
from pydantic_settings import BaseSettings

# Absolute path to the project root directory
# This assumes the script is run from a known location relative to the project root.
# A more robust solution for complex deployments might involve environment variables.
# For this project, we determine the path from this file's location.
# __file__ is backend/app/core/config.py
#
# backend/app/core
core_dir = os.path.dirname(os.path.abspath(__file__))
# backend/app
app_dir = os.path.dirname(core_dir)
# backend/
backend_dir = os.path.dirname(app_dir)

# Now, we construct the absolute path to where the db should be.
# This should be in the `backend` directory.
db_path = os.path.join(backend_dir, "ecommerce.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = SQLALCHEMY_DATABASE_URL

    class Config:
        case_sensitive = True


settings = Settings()