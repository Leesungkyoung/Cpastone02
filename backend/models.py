from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime, Text
from backend.database import Base
import json

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False)
    product_id = Column(Integer, nullable=False)
    top_sensors = Column(String, nullable=False) # Stored as JSON string
    prob = Column(Float, nullable=True)
    resolved = Column(Boolean, default=False, nullable=False)
    resolved_at = Column(DateTime, nullable=True)

    @property
    def top_sensors_list(self):
        return json.loads(self.top_sensors)

    @top_sensors_list.setter
    def top_sensors_list(self, value):
        self.top_sensors = json.dumps(value)

class Setting(Base):
    __tablename__ = "settings"

    key = Column(String, primary_key=True, index=True)
    value = Column(Text, nullable=False)
