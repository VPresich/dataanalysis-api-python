import uuid
from sqlalchemy import Column, String, ForeignKey, Integer, DateTime, func, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class DataSource(Base):
    __tablename__ = "data_sources"

    _id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_user = Column(UUID(as_uuid=True), ForeignKey("users._id", ondelete="CASCADE"), nullable=False)
    number_source = Column(Integer, nullable=False)
    name_source = Column(String, nullable=False)
    name_file = Column(String, nullable=False)
    comments_source = Column(String)
    create_time = Column(DateTime(timezone=True), server_default=func.now())
    update_time = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("id_user", "number_source", name="uq_user_number_source"),
    )
