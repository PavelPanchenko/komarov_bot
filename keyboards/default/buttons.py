import json
from enum import Enum
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class Imenu(Enum):
    new_record: str = '📝Новая запись'
    my_record: str = '📁Мои записи'
    information: str = 'Информация 🧠'
    post_file: str = 'Отправить файл 📇'
    question: str = 'Задать вопрос ❓'


authorization_button = ReplyKeyboardMarkup(resize_keyboard=True, selective=False)
authorization_button.add(KeyboardButton(text='Авторизация 🔓', request_contact=True))

main_menu_buttons = ReplyKeyboardMarkup(resize_keyboard=True, selective=False)
main_menu_buttons.add(KeyboardButton(text='📝Новая запись'))
main_menu_buttons.insert(KeyboardButton(text='📁Мои записи'))
main_menu_buttons.add(KeyboardButton(text='Информация 🧠'))
main_menu_buttons.insert(KeyboardButton(text='Отправить файл 📇'))
main_menu_buttons.add(KeyboardButton(text='Задать вопрос ❓'))

info_menu_buttons = ReplyKeyboardMarkup(resize_keyboard=True, selective=False)
info_menu_buttons.add(KeyboardButton(text='🗓График'))
info_menu_buttons.insert(KeyboardButton(text='🩺Подготовка'))
info_menu_buttons.add(KeyboardButton(text='🛴Как добраться'))
info_menu_buttons.add(KeyboardButton(text='🔙Главное меню'))

support_close_button = ReplyKeyboardMarkup(resize_keyboard=True)
support_close_button.add(KeyboardButton(text='Закончить диалог'))
