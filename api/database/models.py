import datetime

from sqlalchemy import Column, Integer, String, BOOLEAN, ForeignKey, BLOB, DateTime, LargeBinary
from sqlalchemy.orm import relationship, backref

from api.database.base import Base


class Center(Base):
    __tablename__ = "centers"

    id = Column(Integer, primary_key=True)
    address = Column(String)


# centers = Center.__table__


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    tg_id = Column(Integer)
    fullname = Column(String)
    phone_number = Column(String)
    create_at = Column(DateTime, default=datetime.datetime.now())
    records = relationship('Record', backref="users")
    files = relationship('UserFile', backref="users")


# users = User.__table__


class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True)

    location = Column(String)
    date_time = Column(DateTime)
    service = Column(String)
    confirmation = Column(BOOLEAN, default=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    # user = relationship('User', backref="records")


# records = Record.__table__


class UserFile(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True)

    file_name = Column(String)
    file_path = Column(String)
    file_size = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    # user = relationship('User', backref="files")


# files = UserFile.__table__
