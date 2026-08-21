from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from app.database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=True)        # The text of the post
    media_url = Column(String, nullable=True)      # Path to the image/video
    media_type = Column(String, nullable=True)     # 'image' or 'video'
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))