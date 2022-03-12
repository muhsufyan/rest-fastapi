from pydantic import BaseSettings

class Setting(BaseSettings):
    db_hostname: str
    db_port: str
    db_name: str
    db_username: str 
    db_pass: str 
    jwt_secret_key: str 
    jwt_algoritma: str
    jwt_expire: int 
    class Config:
        env_file = ".env"
settings = Setting()