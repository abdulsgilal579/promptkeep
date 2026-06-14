from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from app.db import Base


class InferenceLog(Base):
    __tablename__ = "inference_logs"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    model = Column(String(100), nullable=False)
    prompt = Column(Text, nullable=False)
    output = Column(Text, nullable=False)
    latency_ms = Column(Float, nullable=False)