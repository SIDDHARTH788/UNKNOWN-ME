from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
import shutil
import os
import time
from sqlalchemy import func
from app.database import get_db
from app.models import Post

router = APIRouter()

@router.post("/")
async def create_post(
    content: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    media_url = None
    media_type = None

    # If the user uploaded a file, save it to the /uploads folder
    if file:
        # Create a unique filename so users don't overwrite each other's files
        filename = f"{int(time.time())}_{file.filename}"
        filepath = os.path.join("uploads", filename)
        
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        media_url = f"/uploads/{filename}"
        # Determine if it's an image or video based on the file's content type
        media_type = "image" if file.content_type.startswith("image/") else "video"

    # Create the database record
    new_post = Post(content=content, media_url=media_url, media_type=media_type)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

@router.get("/")
def get_posts(db: Session = Depends(get_db)):
    # Fetch all posts, newest first
    return db.query(Post).order_by(Post.created_at.desc()).all()
@router.get("/stats")
def get_platform_stats(db: Session = Depends(get_db)):
    # Calculate total posts
    total_posts = db.query(Post).count()
    
    # Calculate media breakdown
    image_posts = db.query(Post).filter(Post.media_type == "image").count()
    video_posts = db.query(Post).filter(Post.media_type == "video").count()
    text_only = db.query(Post).filter(Post.media_type == None).count()
    
    return {
        "total_posts": total_posts,
        "images": image_posts,
        "videos": video_posts,
        "text_only": text_only
    }
@router.get("/")
def get_posts(limit: int = 10, offset: int = 0, db: Session = Depends(get_db)):
    # Fetch posts in chunks of 10, skipping the ones we already loaded
    return db.query(Post).order_by(Post.created_at.desc()).offset(offset).limit(limit).all()