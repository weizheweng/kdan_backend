import os
from dotenv import load_dotenv

# 載入對應環境的 .env 文件
env = os.getenv('ENV', 'dev')
load_dotenv(f".env.{env}")

def get_database_url() -> str:
    """獲取資料庫連接字串"""
    if env == 'dev':
        return (
            f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
            f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
        )
    else:
        return (
            f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
            f"@{os.getenv('POSTGRES_HOST')}/{os.getenv('POSTGRES_DB')}"
        )