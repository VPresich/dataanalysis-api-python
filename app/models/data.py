from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class Data(Base):
    __tablename__ = "data"

    _id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid()
    )
    id_source = Column(
        UUID(as_uuid=True),
        ForeignKey("data_sources._id", ondelete="CASCADE"),
        nullable=False,
        name="id_source"
    )

    CVpositive = Column(String, default="None", name="CVpositive")
    CVstable = Column(String, default="None", name="CVstable")
    CApositive = Column(String, default="None", name="CApositive")
    CAstable = Column(String, default="None", name="CAstable")
    CTpositive = Column(String, default="None", name="CTpositive")
    CTstable = Column(String, default="None", name="CTstable")
    X = Column(Float, default=0.0, name="X")
    Y = Column(Float, default=0.0, name="Y")
    Z = Column(Float, default=0.0, name="Z")
    Kde = Column(String, default="None", name="Kde")
    KdeWeighted = Column(String, default="None", name="KdeWeighted")
    Gaussian = Column(String, default="None", name="Gaussian")
    GaussianWeighted = Column(String, default="None", name="GaussianWeighted")
    EvaluationNum = Column(String, default="None", name="EvaluationNum")
    IMMconsistentValue = Column(String, default="None", name="IMMconsistentValue")
    probability = Column(String, default="None", name="probability")
    TrackConsistent = Column(String, default="None", name="TrackConsistent")
    VelocityConsistent = Column(String, default="None", name="VelocityConsistent")
    IMMconsistent = Column(String, default="None", name="IMMconsistent")
    IMMpositive = Column(String, default="None", name="IMMpositive")
    velocityOK = Column(String, default="None", name="velocityOK")
    speed = Column(String, default="None", name="speed")
    TrackNum = Column(Integer, default=0, name="TrackNum")
    Time = Column(Float, default=0.0, name="Time")

    created_at = Column(DateTime(timezone=True), server_default=func.now(), name="created_at")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), name="updated_at")

    source = relationship("DataSource", back_populates="records")
