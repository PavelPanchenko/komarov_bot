from api.database.base import SessionLocal
from api.database.models import Center


def add_address_db(address: str):
    with SessionLocal() as session:
        center = Center(address=address)
        session.add(center)
        session.commit()
        session.refresh(center)
        return center


def get_addresses_db() -> list:
    with SessionLocal() as session:
        return session.query(Center).all()


def get_addresses_by_id_db(address_id) -> Center | None:
    with SessionLocal() as session:
        return session.query(Center).filter(Center.id == address_id).one_or_none()


def update_address_db(address_id: int, address: str):
    with SessionLocal() as session:
        new_address = session.query(Center).filter(Center.id == address_id).update({Center.address: address})
        session.commit()
        return new_address


def delete_address_db(address_id: int):
    with SessionLocal() as session:
        address = session.query(Center).filter(Center.id == address_id).delete()
        session.commit()
        return address

