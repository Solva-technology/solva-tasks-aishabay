from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PRODUCTION: bool = False
    APP_TITLE: str = "Task Manager"
    DESCRIPTION: str = "Система управления задачами для учебных групп"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URL: str
    AUTH_SERVICE_URL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow",
    )


settings = Settings()
