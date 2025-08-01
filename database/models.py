from sqlalchemy import Column, Integer, BigInteger, String, Time, DateTime, func, ForeignKey, Text, CheckConstraint, ARRAY, Boolean
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    name = Column(String)
    wake_up_time = Column(Time)
    sleep_time = Column(Time)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    habits = relationship("Habit", back_populates="user", cascade="all, delete", lazy='selectin')


class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name = Column(Text, nullable=False)
    time_of_day = Column(String, CheckConstraint("time_of_day IN ('morning', 'afternoon', 'evening', 'any')"), nullable=False)
    frequency_type = Column(String, CheckConstraint("frequency_type IN ('hourly', 'daily', 'weekly', 'custom')"), nullable=False)
    days_of_week = Column(ARRAY(Text))
    reminder_enabled = Column(Boolean, default=False)
    reminder_time = Column(Time)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    image_file_id = Column(Text)
    hourly_start = Column(Time)
    hourly_end = Column(Time)

    user = relationship("User", back_populates="habits", lazy='joined')


class Habit_templates(Base):
    __tablename__ = "habit_templates"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    time_of_day = Column(String, CheckConstraint("time_of_day IN ('morning', 'afternoon', 'evening', 'any')"), nullable=False)
    frequency_type = Column(String, CheckConstraint("frequency_type IN ('hourly', 'daily', 'weekly', 'custom')"), nullable=False)
    days_of_week = Column(ARRAY(Text))
    reminder_time = Column(Time)
    is_active = Column(Boolean, default=True, nullable=False)
    image_file_id = Column(Text)
    hourly_start = Column(Time)
    hourly_end = Column(Time)
    emoji = Column(Text)


