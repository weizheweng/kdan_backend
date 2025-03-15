from fastapi import FastAPI
from .database import Base, engine
from .routers import pharmacies, users, search
from fastapi.middleware.cors import CORSMiddleware

# 若想在首次啟動時自動建表 (僅開發環境建議)
# 不建議生產環境自動執行，避免破壞既有資料
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Pharmacy Platform API",
    description="Pharmacy Platform API",
    version="1.0.0"
)

origins = [
    "http://localhost:3000",
    "https://weizheweng.github.io"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 將路由掛進主 app
app.include_router(pharmacies.router)
app.include_router(users.router)
app.include_router(search.router)