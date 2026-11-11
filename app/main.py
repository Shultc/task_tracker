from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# Отключаем редиректы с / на /
app = FastAPI(
    title="Task Tracker API",
    version="1.0.0",
    redirect_slashes=False  # ← ключевое изменение
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Импорты роутеров
from app.routers.tasks import router as tasks_router
from app.routers.projects import router as projects_router
from app.routers.users import router as users_router
from app.routers.auth import router as auth_router

app.include_router(users_router)
app.include_router(projects_router)
app.include_router(tasks_router)
app.include_router(auth_router)


@app.get("/")
async def root():
    return {"message": "Task Tracker API is running"}
