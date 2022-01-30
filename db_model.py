from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pathlib import Path


# 02 create first level, engine
dir_absolute_path = str(Path().absolute())
engine = create_engine("sqlite:///" + dir_absolute_path + "/data.db")

# 03 create Base class model
Base = declarative_base()

# 04 create Student model (db table)
class Student_Db_Model(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    gender = Column(String)


def create_database():
    Base.metadata.create_all(engine)
