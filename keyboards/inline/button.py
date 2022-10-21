from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from utils.static_data import list_services

callback_center = CallbackData('center', 'event', 'payload')
callback_service = CallbackData('service', 'event', 'payload')
callback_record = CallbackData('record', 'event', 'payload')
callback_file = CallbackData('file', 'event', 'payload')


def location_items(locations, event: str = 'center_list'):
    markup = InlineKeyboardMarkup()
    for center in locations:
        address = center['address']
        markup.add(InlineKeyboardButton(
            text=f"🔴 {address}" if 'москва' in str(address).lower() else f"🔵 {address}",
            callback_data=callback_center.new(event=event, payload=center['id'])))
    return markup


def services_items(event: str = 'service'):
    markup = InlineKeyboardMarkup()
    for service in list_services:
        markup.add(InlineKeyboardButton(
            text=service['category'],
            callback_data=callback_service.new(event=event, payload=service['id'])))
    return markup


accept_appointment_button = InlineKeyboardMarkup()
accept_appointment_button.add(
    InlineKeyboardButton(text='Отправить', callback_data=callback_center.new(event='send_data', payload='send')))
accept_appointment_button.add(
    InlineKeyboardButton(text='Отредактировать', callback_data=callback_center.new(event='send_data', payload='edit')))


def accept_record_button(record_id: int, accepted_btn: bool = True):
    markup = InlineKeyboardMarkup()
    if accepted_btn:
        markup.add(
            InlineKeyboardButton(
                text='Подтвердить', callback_data=callback_record.new(event='accept_record', payload=str(record_id))))

    markup.insert(
        InlineKeyboardButton(
            text='Отклонить',
            callback_data=callback_record.new(event='reject_record', payload=str(record_id))
        ))
    return markup


def my_record_list_button(record_id: int):
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton(
        text='Отменить',
        callback_data=callback_record.new(event='cancel_record', payload=record_id)))

    return markup


def callback_button(user_id):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text='Написать', callback_data=callback_file.new(event='callback', payload=user_id)))
    return markup


admin_menu_button = InlineKeyboardMarkup()
admin_menu_button.add(InlineKeyboardButton(text='Записи', callback_data='menu_record'))
admin_menu_button.add(InlineKeyboardButton(text='Написать всем', callback_data='send_all_message'))

admin_menu_record_button = InlineKeyboardMarkup()
admin_menu_record_button.add(InlineKeyboardButton(text='Подтвержденные', callback_data='menu_record_items'))
admin_menu_record_button.add(InlineKeyboardButton(text='Не подтвержденные', callback_data='menu_not_record_items'))
admin_menu_record_button.add(InlineKeyboardButton(text='🔙 Назад', callback_data='admin_menu'))

admin_cancel_message_all_users_button = InlineKeyboardMarkup()
admin_cancel_message_all_users_button.add(InlineKeyboardButton(text='🔙 Назад', callback_data='admin_menu'))
