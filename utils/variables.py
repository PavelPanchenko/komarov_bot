authorization_message = """<pre>
🤖 Добро пожаловать {}!
Авторизуйтесь пожалуйста.
</pre>
"""

main_menu_message = "<pre>Главное меню</pre>"

success_authorization_message = "<pre>✅ Авторизация прошла успешно</pre>"
error_authorization_message = "<pre>Доступ запрещен ⛔</pre>"

loading_icon = r'CAACAgIAAxkBAAJNN2I3GMOSOBp9h5OH-kDsCF71w8t-AAJDAQACzRswCIC-idiBA72TIwQ'

record_to_center_message = '<pre>🔎В какой центр удобно записаться ?</pre>'
date_to_center_message = '<pre>Выберите дату приема:</pre>'
time_to_center_message = """
<pre>Пришлите желаемое время на прием</pre>
<pre>в формате: hh:mm</pre>
"""

service_message = "<pre>На какую услугу хотите записаться ?</pre>"

data_to_center_message = """<pre>
<i>Запись на прием:</i>
<b>Адрес: </b>{}
<b>Дата: </b>{}
<b>Время: </b>{}
<b>Услуга: </b>{}
</pre>
"""

send_data_record = "<pre>Запись отправлена.\nОжидайте подтверждения от специалистов</pre>"
success_confirm_record = "<pre>Запись подтверждена.\nМы вас ожидаем\n{}</pre>"
reject_confirm_record = "<pre>Запись\nна {} \nотклонена.\nЗапишитесь повторно</pre>"
reject_confirm_user_record = "<pre>Запись № {} отменена пользователем</pre>"
for_all_users_message = 'Введите сообщение , которое хотите отправить всем'
users_empty_message = 'В данный момент нет ни одного получателя'

not_record_list_message = '<pre>У вас нет записей</pre>'

confirmed_rec_message = "<pre>Подтвержденных записей нет.</pre>"

unconfirmed_rec_message = "<pre>Неподтвержденных записей нет.</pre>"

send_admins_record_message = """
<code><b>Запись №</b> <i>{}</i>
<b>Клиент:</b></code> <i>{}</i>
<code><b>Дата:</b> <i>{}</i>
<b>Услуга:</b> <i>{}</i>
<b>Адрес:</b> <i>{}</i>
</code>
"""

send_client_record_message = """<pre>
<b>Запись</b> <i>№{}</i>
<b>Дата:</b> <i>{}</i>
<b>Услуга:</b> <i>{}</i>
<b>Адрес:</b> <i>{}</i>
<b>Статус:</b> <i>{}</i>
</pre>
"""

closed_time_message = "<pre>В данное время мы не работаем.\nВыберите другое время</pre>"

opening_hours_message = """
<b>🗓График работы</b>:

<b>🔵Санкт-Петербург</b>
🔹 Лиговский пр., д. 78
   ПН - ВС: 08:00 - 20:00  
   Spb1@mc-medprof.ru

🔹 ул. Малая Балканская, д. 26  
   ПН-ПТ с 08:00-18:00
   Spb2@mc-medprof.ru 

🔹 пр. Просвещения, 23, лит. А
   ПН-ПТ с 08:00-20:00
   СБ с 09:00-17:00
   ВС выходной
   Spb3@mc-medprof.ru  

🔹 пр. Большевиков, д. 7, к. 2, стр. 1  
   ПН-ПТ с 08:00-20:00 
   СБ с 09:00-17:00 
   ВС выходной 
   Spb4@mc-medprof.ru 

<b>🔴Москва</b>        
🔺 ВДНХ  ул. Бориса Галушкина, д. 3
   ПН-ПТ с 08:30-17:30
   info-msk@mc-medprof.ru
"""

send_document_message = "<pre>📎 Пришлите необходимый файл</pre>"

error_format_files_message = "<pre>Файл должен быть форматом document или photo</pre>"
success_format_files_message = "<pre>Файл успешно передан ✅</pre>"

support_start_message = "<pre>Напишите свой вопрос</pre>"
error_message = '<pre>Что бы задать вопрос воспользуйтесь специальной кнопкой</pre>'

not_edit_record_message = "<pre>Эта запись уже была отправлена</pre>"
