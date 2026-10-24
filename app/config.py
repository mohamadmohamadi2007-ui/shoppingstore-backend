from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./shop.db"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


    # class Config:
    #     env_file = ".env"


settings = Settings()