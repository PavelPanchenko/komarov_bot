import json

from pydantic import BaseModel


class ICenterAddresses(BaseModel):
    id: int
    address: str


center_addresses = json.dumps([
    {
        'id': 1,
        'address': 'СПБ, Лиговский, 78'
    },
    {
        'id': 2,
        'address': 'СПБ, Малая Балканская, 26'
    },
    {
        'id': 3,
        'address': 'СПБ, Просвещения, 23'
    },
    {
        'id': 4,
        'address': 'СПБ, Большевиков, 7'
    },
    {
        'id': 4,
        'address': 'Москва, Бориса Галушкина, 3'
    },
])

list_services = [
    {
        'id': 1,
        'category': 'Проф осмотры',
        'description': 'При себе иметь паспорт'
    },
    {
        'id': 2,
        'category': 'ЛМК',
        'description': 'При себе иметь паспорт'
    },
    {
        'id': 3,
        'category': 'Продление ЛМК',
        'description': 'При себе иметь паспорт'
    },
    {
        'id': 4,
        'category': 'Психиатрическое освидетельствование',
        'description': 'При себе иметь паспорт'
    },
    {
        'id': 5,
        'category': 'Иностранные граждане',
        'description': 'При себе иметь паспорт'
    },
    {
        'id': 6,
        'category': 'Комиссия плав состава',
        'description': ''
    },
    {
        'id': 7,
        'category': 'Справки',
        'description': 'При себе иметь паспорт'
    },
    {
        'id': 8,
        'category': 'Водительская комиссия',
        'description': 'При себе иметь паспорт'
    },
    {
        'id': 9,
        'category': 'Вакцинация',
        'description': 'При себе иметь паспорт'
    },
    {
        'id': 10,
        'category': 'Ковид',
        'description': 'При себе иметь паспорт'
    },
    {
        'id': 11,
        'category': 'ФЛГ',
        'description': 'При себе иметь паспорт'
    },
]
