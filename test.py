from sqlalchemy import create_engine, Column, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import enum

DATABASE_URI = 'mysql://ac_user:172003@localhost/ac_users'
engine = create_engine(DATABASE_URI)
Base = declarative_base()

class UserType(enum.Enum):
    user = "user"
    admin = "admin"

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    user_type = Column(Enum(UserType), default=UserType.user)

Session = sessionmaker(bind=engine)
session = Session()

users = session.query(User).all()
for user in users:
    print(f'ID: {user.id}, Username: {user.username}, Email: {user.email}, Type: {user.user_type.value},  Hash: {user.password}')
