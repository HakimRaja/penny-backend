from functools import lru_cache
from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL:str
    SECRET_KEY:str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    REFRESH_TOKEN_EXPIRE_DAYS:int

    model_config=SettingsConfigDict(env_file='.env',extra='ignore')

# Use lru_cache to ensure the settings object is loaded only once
@lru_cache()
def get_settings():
    return Settings()

# Instantiate the settings object for use in other modules
settings = get_settings()