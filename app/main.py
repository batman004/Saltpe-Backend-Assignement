import uvicorn
import databases
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.users.endpoints.routers import router as user_router

# importing server settings
from api.config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database = databases.Database(settings.DB_URL)


@app.get("/")
def read_root():
    return {"message": "welcome to salt-task-backend"}


# initialising motor client on server startup
@app.on_event("startup")
async def startup_db_client():

    await database.connect()


@app.on_event("shutdown")
async def shutdown_db_client():

    await database.disconnect()


app.include_router(user_router, tags=["users"], prefix="/user")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        reload=settings.DEBUG_MODE,
        port=settings.PORT,
    )
