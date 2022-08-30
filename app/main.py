import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware
from api.users.endpoints.routers import router as user_router

# importing server settings
from api.config import settings

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=settings.DB_URL_DEV)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "welcome to salt-task-backend"}


@app.on_event("shutdown")
def clear_blacklist_db():
    with open("api/users/utils/blacklist_db.txt", "w") as file:
        pass


app.include_router(user_router, tags=["users"], prefix="/user")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        reload=settings.DEBUG_MODE,
        port=settings.PORT,
    )
