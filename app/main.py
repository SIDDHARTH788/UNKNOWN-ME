from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.posts import router as posts_router
import os

from app.api.chat import router as chat_router
from app.database import engine, Base

# Create the database tables automatically
Base.metadata.create_all(bind=engine)

# Ensure the uploads directory exists
os.makedirs("uploads", exist_ok=True)

app = FastAPI(
    title="Anonymous Support & Social Network",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the 'uploads' folder so images/videos can be accessed via URL
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(chat_router, prefix="/api")
app.include_router(posts_router, prefix="/api/posts")

@app.get("/")
async def root():
    return {"message": "Server is running with Database integration."}