from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class CallLog(Base):
    __tablename__ = 'call_logs'
    id = Column(Integer, primary_key=True)
    call_sid = Column(String(50), unique=True)
    caller_phone = Column(String(20))
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    transcript = Column(Text)
    summary = Column(Text)
    intent = Column(String(50))
    status = Column(String(20)) # completed, failed, busy

class Lead(Base):
    __tablename__ = 'leads'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    phone = Column(String(20))
    service_required = Column(String(200))
    interest_level = Column(String(20)) # Hot, Normal, Cold
    created_at = Column(DateTime, default=datetime.utcnow)
    call_id = Column(Integer, ForeignKey('call_logs.id'))

class Appointment(Base):
    __tablename__ = 'appointments'
    id = Column(Integer, primary_key=True)
    customer_name = Column(String(100))
    phone = Column(String(20))
    service_type = Column(String(100))
    appointment_time = Column(DateTime)
    status = Column(String(20)) # scheduled, cancelled, completed
    created_at = Column(DateTime, default=datetime.utcnow)
