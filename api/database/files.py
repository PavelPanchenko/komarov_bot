from api.database.base import SessionLocal
from api.database.models import UserFile
from api.database.user import get_user_db


def add_file_db(tg_id: int, file_name: str, file_content: bytes):
    with SessionLocal() as session:
        user = get_user_db(tg_id=tg_id)
        file = UserFile(file_name=file_name, file_content=file_content, user_id=user.id)
        session.add(file)
        session.commit()
        session.refresh(file)
        return file


def get_files_by_tg_id_db(tg_id: int):
    with SessionLocal() as session:
        return session.query(UserFile).all()
        # files = session.query(UserFile).filter(UserFile.user_id)
