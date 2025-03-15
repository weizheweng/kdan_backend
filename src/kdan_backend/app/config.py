import os
from dotenv import load_dotenv

# 載入對應環境的 .env 文件
load_dotenv()

# 如果有指定環境變數，則再載入對應的環境設定檔
env = os.getenv('ENV')
if env:
    load_dotenv(f".env.{env}", override=True)

def get_database_url() -> str:
    """獲取資料庫連接字串"""
    return (
            f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
            f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
        )
    