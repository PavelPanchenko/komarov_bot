
from api.database.base import SessionLocal
from api.database.models import UserFile
from api.database.user import get_user_db


def add_file_db(tg_id: int, file_name: str, file_path: str, file_size: str):
    with SessionLocal() as session:
        # user = get_user_db(tg_id=tg_id)
        file = UserFile(file_name=file_name, file_path=file_path, file_size=file_size, user_id=tg_id)
        session.add(file)
        session.commit()
        session.refresh(file)
        return file


def get_all_files():
    with SessionLocal() as session:
        return session.query(UserFile).all()


def get_files_by_id_db(file_id: int):
    with SessionLocal() as session:
        files = session.query(UserFile).filter(UserFile.id == file_id).first()
        return files


def delete_file_db(file_id: int):
    with SessionLocal() as session:
        session.query(UserFile).filter(UserFile.id == file_id).delete()
        session.commit()
