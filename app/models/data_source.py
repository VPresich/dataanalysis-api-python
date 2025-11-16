import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, UniqueConstraint, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.sql import func


class DataSource(Base):
    __tablename__ = "data_sources"

    _id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_user = Column(UUID(as_uuid=True), ForeignKey("users._id", ondelete="CASCADE"), nullable=False)
    source_number = Column(Integer, nullable=False)
    source_name = Column(String(255), nullable=False)
    file_name = Column(String(255), nullable=False)
    comment = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("id_user", "source_number", name="uq_user_number_source"),
    )

    user = relationship("User", back_populates="data_sources")
