from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )

    DATABASE_URL: str

    @field_validator('DATABASE_URL')
    @classmethod
    def preparar_url_sqlite(cls, url: str):
        if url.startswith('sqlite:///'):
            return url.replace('sqlite:///', 'sqlite+aiosqlite:///', 1)
        return url
