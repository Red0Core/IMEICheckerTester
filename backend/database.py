from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, create_engine
from datetime import datetime
from .config import DATABASE_URL

engine = create_engine(DATABASE_URL)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String, nullable=False)
    refresh_tokens = relationship("RefreshToken", back_populates="owner")

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    expires_at = Column(DateTime, nullable=False)

    owner = relationship("User", back_populates="refresh_tokens")

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db  # Открываем сессию
    finally:
        db.close()
