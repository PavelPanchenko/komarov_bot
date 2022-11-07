import sqlalchemy
from sqlalchemy.orm import declarative_base, sessionmaker
from settings.config import DATABASE_NAME


# DATABASE_URL = f"sqlite:///{DATABASE_NAME}"
# # DATABASE_URL = f"postgresql://root:12345@pavel-panchenko.tmweb.ru/users"
#
# # engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# engine = sqlalchemy.create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# Base = declarative_base()




