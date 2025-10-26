import uuid
from sqlalchemy import Column, ForeignKey, Enum, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
from .enums import ThemeEnum
from .enums import AppEnum


class Theme(Base):
    __tablename__ = "themes"

    _id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users._id", ondelete="CASCADE"), nullable=False)
    color = Column(Enum(ThemeEnum), nullable=False, default=ThemeEnum.yellow)
    app = Column(Enum(AppEnum), nullable=False, default=AppEnum.teachers)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
