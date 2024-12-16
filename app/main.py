from fastapi import FastAPI
from api.repos import router as repos_router

app = FastAPI()

# Подключение маршрутов
app.include_router(repos_router, prefix="/api/repos", tags=["Repositories"])