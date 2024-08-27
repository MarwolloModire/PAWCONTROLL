from sqlalchemy import Column, Integer, String, DateTime, Time, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func
from config import settings
from datetime import datetime

Base = declarative_base()


class WalkOrder(Base):
    __tablename__ = "walk_orders"

    id = Column(Integer, primary_key=True, index=True)
    apartment_number = Column(String, nullable=False, index=True)
    pet_name = Column(String, nullable=False)
    pet_breed = Column(String, nullable=False)
    walk_date = Column(DateTime, nullable=False, index=True)
    walk_time = Column(Time, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    @property
    def formatted_walk_date(self):
        # Форматирование даты (для улучшения восприятия человеком)
        return self.walk_date.strftime('%Y-%m-%d')

    @property
    def formatted_created_at(self):
        # Форматирование даты и времени (для улучшения восприятия человеком)
        return self.created_at.strftime('%Y-%m-%d %H:%M:%S')

    def to_dict(self):
        return {
            "id": self.id,
            "apartment_number": self.apartment_number,
            "pet_name": self.pet_name,
            "pet_breed": self.pet_breed,
            "walk_date": self.formatted_walk_date,
            # Форматирование времени (для улучшения восприятия человеком)
            "walk_time": self.walk_time.strftime('%H:%M:%S'),
            "created_at": self.formatted_created_at
        }


# Создание подключения к базе данных и сессии
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание всех таблиц в базе данных
Base.metadata.create_all(bind=engine)
