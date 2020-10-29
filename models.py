from sqlalchemy import create_engine,MetaData,Column,Integer,Float,String,Table,ForeignKey,UniqueConstraint,Index,TIMESTAMP,Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy import create_engine
import time
engine  = create_engine("mysql+pymysql://root:8597121@127.0.0.1:3306/test", max_overflow=5)
Base = declarative_base()
class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True)
    name = Column(String(10))
    password = Column(Integer)
    email = Column(Integer,unique=True)
    score = Column(Integer)

class Code(Base):
    __tablename__ = 'code'
    id = Column(Integer, primary_key=True,autoincrement=True)
    code = Column(String(4))
    expire_date = Column(Integer)
    is_register = Column(Integer)
class CPU(Base):
    __tablename__ = 'cpu'
    id = Column(Integer,primary_key=True)
    cpu = Column(Float)
    password = Column(Integer)
    email = Column(Integer,unique=True)
    score = Column(Integer)
def init_db():
    Base.metadata.create_all(engine)
def drop_db():
    Base.metadata.drop_all(engine)
init_db()
Session = sessionmaker(bind=engine)
session = Session()
