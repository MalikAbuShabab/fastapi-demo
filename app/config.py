from pydantic import BaseSettings

class Settings(BaseSettings):
    API_VERSION: str 
    API_TITLE: str 
    database_username: str 
    database_password: str 
    database_host: str
    database_port: int 
    database_name: str 
    secret_key: str 
    debug: bool
    algorithm: str 
    access_token_expiration: int 

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()



