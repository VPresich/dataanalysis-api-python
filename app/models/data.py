from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base


class Data(Base):
    __tablename__ = "data"

    _id = Column(Integer, primary_key=True, index=True)
    id_source = Column(Integer, ForeignKey("data_sources._id", ondelete="CASCADE"), nullable=False)

    CVpositive = Column(String, default="None")
    CVstable = Column(String, default="None")
    CApositive = Column(String, default="None")
    CAstable = Column(String, default="None")
    CTpositive = Column(String, default="None")
    CTstable = Column(String, default="None")
    X = Column(Float, default=0.0)
    Y = Column(Float, default=0.0)
    Z = Column(Float, default=0.0)
    Kde = Column(String, default="None")
    KdeWeighted = Column(String, default="None")
    Gaussian = Column(String, default="None")
    GaussianWeighted = Column(String, default="None")
    EvaluationNum = Column(String, default="None")
    IMMconsistentValue = Column(String, default="None")
    probability = Column(String, default="None")
    TrackConsistent = Column(String, default="None")
    VelocityConsistent = Column(String, default="None")
    IMMconsistent = Column(String, default="None")
    IMMpositive = Column(String, default="None")
    velocityOK = Column(String, default="None")
    speed = Column(String, default="None")
    TrackNum = Column(Integer, default=0)
    Time = Column(Float, default=0.0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    source = relationship("DataSource", back_populates="data")
