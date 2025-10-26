import uuid
from sqlalchemy import Column, String, Boolean, Enum, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
from .enums import ThemeEnum


class User(Base):
    __tablename__ = "users"

    _id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(32), nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    token = Column(String, default=None)
    avatar_url = Column(String, nullable=False)
    verify = Column(Boolean, default=False)
    verification_token = Column(String, nullable=False)
    theme = Column(Enum(ThemeEnum, name="theme_enum"), nullable=False)
    google_id = Column(String, unique=True, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
