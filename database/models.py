from sqlalchemy import Column, Integer, String
from .database import Base

class Appointment(Base):
    __tablename__ = "appointments"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_name = Column(String, nullable=False)
    doctor_name = Column(String, nullable=False)
    appointment_date = Column(String, nullable=False)  # Store as ISO format (YYYY-MM-DD HH:MM)
    status = Column(String, default="Scheduled") # Status: Scheduled, Completed, Cancelled
