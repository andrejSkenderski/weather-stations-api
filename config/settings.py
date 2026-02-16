from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    redis_url: str
    valid_username: str
    valid_password: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    csv_host_path: str
    csv_container_file_path: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
