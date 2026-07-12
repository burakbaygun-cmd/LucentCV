from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "LucentCV 2.0"
    API_V1_STR: str = "/api"
    
    # Gemini
    GEMINI_API_KEY: str
    
    # Supabase
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str = ""
    SUPABASE_SERVICE_ROLE_KEY: str = ""

    class Config:
        env_file = ".env"
        extra = "allow"
        case_sensitive = True

settings = Settings()
