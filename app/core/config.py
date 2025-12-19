from pydantic_settings import BaseSettings
from pydantic import BaseModel
from pathlib import Path

BASEDIR = Path(__file__).parent.parent

class Settings():
    url: str = 'postgresql+asyncpg://neondb_owner:npg_qruiahe0dnL4@ep-steep-dew-agw1y9c7-pooler.c-2.eu-central-1.aws.neon.tech/neondb'
    echo: bool = False
    
settings = Settings()