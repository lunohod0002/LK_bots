import telebot


from app.services.keywords import get_keywords,get_names
import json
from app.services import get_current_names, get_current_brands, get_brand_current_names

from telebot.types import ReplyKeyboardRemove, Message
from app.services import storage, get_all_id, get_all_names, get_all_brands, get_all_types,get_keywords_list
from app.keyboards.catalog import gen_main_keyboard, gen_search_keyboard, \
    get_info_brand, gen_second_keyboard, gen_third_keyboard, get_info, get_brands_keyboard, \
    get_second_brand_keybord, get_mail_keyboard, get_manual_keyboard
from app.keyboards.start import user_start_keyboard, admin_start_keybooard
from app.keyboards.search import search_info, gen_search_keyboard

from main import bot,admin_id
from app.handlers.start import start

keys = []

kol = 0
with open('app/services/equipment.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'mail':
        if int(call.message.chat.id) == int(admin_id):
            bot.send_message(call.from_user.id, "Напишите сообщение всем пользователям",reply_markup=ReplyKeyboardRemove())
            storage.set_state(chat_id=call.message.chat.id, user_id=call.from_user.id, state='send_mail')

    elif call.data == 'catalog_types':
        bot.send_message(call.from_user.id, "Выберите тип прибора",
                         reply_markup=gen_main_keyboard())
        storage.reset_data(chat_id=call.message.chat.id, user_id=call.from_user.id)

        storage.set_state(chat_id=call.message.chat.id, user_id=call.from_user.id, state='choose_type')
        bot.answer_callback_query(callback_query_id=call.id, show_alert=True)
    elif call.data == 'catalog_brands':
        bot.send_message(call.from_user.id, "Выберите бренд прибора",
                         reply_markup=get_brands_keyboard())
        storage.reset_data(chat_id=call.message.chat.id, user_id=call.from_user.id)

        storage.set_state(chat_id=call.message.chat.id, user_id=call.from_user.id, state='brand_type')
        bot.answer_callback_query(callback_query_id=call.id, show_alert=True)
    elif call.data == 'search':

        bot.send_message(call.from_user.id, "Напишите название прибора",
                         reply_markup=ReplyKeyboardRemove())
        storage.reset_data(chat_id=call.message.chat.id, user_id=call.from_user.id)

        storage.set_state(chat_id=call.message.chat.id, user_id=call.from_user.id, state='search')
        bot.answer_callback_query(callback_query_id=call.id, show_alert=True)
    elif call.data in get_all_names():
        bot.send_message(call.from_user.id, search_info(call.data), reply_markup=get_manual_keyboard(call.data))
        storage.reset_data(chat_id=call.message.chat.id, user_id=call.from_user.id)

        storage.set_state(chat_id=call.message.chat.id, user_id=call.from_user.id, state='search')
        bot.answer_callback_query(callback_query_id=call.id, show_alert=True)
    elif call.data == "menu":

        if call.message.chat.id == int(admin_id):
            bot.send_message(call.message.chat.id, "Привет! Нажми на кнопку, чтобы начать",
                             reply_markup=admin_start_keybooard())
        else:
            bot.send_message(call.message.chat.id, "Привет! Нажми на кнопку, чтобы начать",
                             reply_markup=user_start_keyboard())
        storage.reset_data(chat_id=call.message.chat.id, user_id=call.from_user.id)

        storage.set_state(chat_id=call.message.chat.id, user_id=call.from_user.id, state='choose_button')
        bot.answer_callback_query(callback_query_id=call.id, show_alert=True)
    elif call.data == "send":
        answer = storage.get_data(chat_id=call.message.chat.id, user_id=call.from_user.id)['mail']
        users_id = get_all_id()
        bot.edit_message_text(text="Сообщение отправлено", chat_id=int(admin_id), message_id=call.message.id)

        for id in users_id:
            bot.send_message(int(id), answer)

        storage.set_state(chat_id=call.message.chat.id, user_id=call.from_user.id,
                          state='sended_mail')
    elif call.data == "change":
        bot.edit_message_text(text="Измените сообщение", chat_id=int(admin_id), message_id=call.message.id)

        storage.set_state(chat_id=call.message.chat.id, user_id=call.from_user.id,
                          state='send_mail')
    elif call.data == "cancel":
        bot.edit_message_text(text="Рассылка отменена", chat_id=int(admin_id), message_id=call.message.id)
        storage.set_state(chat_id=call.message.chat.id, user_id=call.from_user.id,
                          state='choose_button')


@bot.message_handler(content_types=['text'])
def search(message: Message):
    if storage.get_state(chat_id=message.chat.id, user_id=message.from_user.id) == 'send_mail':
        bot.send_message(chat_id=int(admin_id), text=f"Ваше сообщение: {message.text}", reply_markup=get_mail_keyboard())
        storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                         key='mail', value=message.text)
        storage.set_state(chat_id=message.chat.id, user_id=message.from_user.id,
                          state='sending_mail')

    match storage.get_state(chat_id=message.chat.id, user_id=message.from_user.id):
        case 'search':
            if (len(message.text) > 1):
                lis = list()
                names = get_names()

                keywords=get_keywords()
                for i in range(len(names)):
                    keyword=keywords[i]
                    keyword = list(map(lambda x: x.lower(), keyword))
                    if message.text.lower() in names[i].lower() or message.text.lower() in keyword:
                        lis.append(names[i])


                if len(lis) == 0:
                    bot.send_message(message.chat.id, "Название не найдено", reply_markup=gen_search_keyboard(lis))
                else:
                    bot.send_message(message.chat.id, text=f"Найдено {len(lis)} совпадений",
                                     reply_markup=gen_search_keyboard(lis))
                    storage.set_state(chat_id=message.chat.id, user_id=message.from_user.id,
                                      state='search')

            else:
                bot.send_message(message.chat.id, "Название должно быть длинее 1 символов")



        case 'brand_type':
            brands = get_all_brands()
            if message.text in brands:
                bot.send_message(message.chat.id, "Выбери название прибора",
                                 reply_markup=get_second_brand_keybord(message.text))
                storage.set_state(chat_id=message.chat.id, user_id=message.from_user.id,
                                  state='brand_name')
                storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                 key='brand_type', value=message.text)
            elif message.text == 'Меню':
                if message.chat.id == int(admin_id):
                    bot.send_message(message.chat.id, "Привет! Нажми на кнопку, чтобы начать",
                                     reply_markup=admin_start_keybooard())
                else:
                    bot.send_message(message.chat.id, "Привет! Нажми на кнопку, чтобы начать",
                                     reply_markup=user_start_keyboard())

                storage.reset_data(chat_id=message.chat.id, user_id=message.from_user.id)

                storage.set_state(chat_id=message.chat.id, user_id=message.from_user.id, state='choose_button')
            else:
                bot.send_message(message.chat.id, "Выберите бренд прибора")

        case 'brand_name':
            brand = storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['brand_type']
            names = get_brand_current_names(brand=brand)
            if (message.text in names):
                storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                 key='brand_name', value=message.text)
                bot.send_message(message.chat.id, get_info_brand(tg_id=message.chat.id),
                                 reply_markup=get_manual_keyboard(message.text))
            elif (message.text == '\U0001F519Назад'):
                bot.send_message(message.chat.id, "Выберите бренд прибора",
                                 reply_markup=get_brands_keyboard())
                storage.set_state(chat_id=message.chat.id, user_id=message.from_user.id,
                                  state='brand_type')
            else:
                bot.send_message(message.chat.id, "Название не найдено")

        case 'choose_type':
            if (message.text in get_all_types()):
                bot.send_message(message.chat.id, "Выбери бренд прибора",
                                 reply_markup=gen_second_keyboard(message.text))
                storage.set_state(chat_id=message.chat.id, user_id=message.from_user.id,
                                  state='choose_brand')
                storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                 key='type', value=message.text)
            elif (message.text == 'Меню'):
                if message.chat.id == int(admin_id):
                    bot.send_message(message.chat.id, "Привет! Нажми на кнопку, чтобы начать",
                                     reply_markup=admin_start_keybooard())
                else:
                    bot.send_message(message.chat.id, "Привет! Нажми на кнопку, чтобы начать",
                                     reply_markup=user_start_keyboard())

                storage.reset_data(chat_id=message.chat.id, user_id=message.from_user.id)

                storage.set_state(chat_id=message.chat.id, user_id=message.from_user.id, state='choose_button')
            else:
                bot.send_message(message.chat.id, "Ошибка. Поробуй еще раз")

        case 'choose_brand':
            type = storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['type']
            brands = get_current_brands(type=type)
            if (message.text in brands):
                storage.set_state(chat_id=message.chat.id, user_id=message.from_user.id,
                                  state='choose_name')
                storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                 key='brand', value=message.text)
                bot.send_message(message.chat.id, "Выбери название прибора",
                                 reply_markup=gen_third_keyboard(message.from_user.id))
            elif (message.text == '\U0001F519Назад'):
                bot.send_message(message.chat.id, "Выбери тип прибора",
                                 reply_markup=gen_main_keyboard())

                storage.reset_data(chat_id=message.chat.id, user_id=message.from_user.id)
                storage.set_state(chat_id=message.chat.id, user_id=message.from_user.id,
                                  state='choose_type')
            else:
                bot.send_message(message.chat.id, "Бренд не найден. Попробуй еще раз")
        case 'choose_name':
            type = storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['type']
            brand = storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['brand']
            names = get_current_names(type=type, brand=brand)
            if (message.text in names):
                storage.set_state(chat_id=message.chat.id, user_id=message.from_user.id,
                                  state='choose_name')
                storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                 key='name', value=message.text)
                bot.send_message(message.chat.id, get_info(message.from_user.id),
                                 reply_markup=get_manual_keyboard(message.text))
            elif (message.text == 'Новый запрос'):
                bot.send_message(message.chat.id, "Выбери тип прибора",
                                 reply_markup=gen_main_keyboard())
                storage.reset_data(chat_id=message.chat.id, user_id=message.from_user.id)
                storage.set_state(chat_id=message.chat.id, user_id=message.from_user.id,
                                  state='choose_type')
            elif (message.text == '\U0001F519Назад'):
                bot.send_message(message.chat.id, "Выбери бренд прибора",
                                 reply_markup=gen_second_keyboard(
                                     storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)[
                                         'type']))
                storage.set_state(chat_id=message.chat.id, user_id=message.from_user.id,
                                  state='choose_brand')
            else:
                bot.send_message(message.chat.id, "Название не найдено. Поробуй еще раз")
        case 'complete':
            if (message.text == 'Новый запрос'):
                bot.send_message(message.chat.id, "Выбери тип прибора",
                                 reply_markup=gen_main_keyboard())
                storage.reset_data(chat_id=message.chat.id, user_id=message.from_user.id)
                storage.set_state(chat_id=message.chat.id, user_id=message.from_user.id,
                                  state='choose_type')


bot.set_chat_menu_button()
