from app.services.types import equipment_catalog
import telebot
from app.services.brands import brands
from telebot.types import ReplyKeyboardRemove, Message
from app.services.names import equipment
from app.services import storage
from app.services.keys import keys3
from app.keyboards import gen_main_keyboard, gen_search_keyboard, gen_first_keyboard, \
    gen_second_keyboard, gen_third_keyboard, get_info, search_info, get_brands_keyboard, get_second_brand_keybord, \
    get_info_brand
from main import bot

keys = []
for key in equipment_catalog.keys():
    keys.append(key)
keys2 = []
for key in equipment.keys():
    keys2.append(key)
kol = 0


@bot.message_handler(commands=['start'])
def start(message: Message):
    bot.send_message(message.chat.id, "Привет! Нажми на кнопку, чтобы начать", reply_markup=gen_first_keyboard())

    storage.reset_data(chat_id=message.chat.id, user_id=message.from_user.id)
    storage.set_state(chat_id=message.chat.id, user_id=message.from_user.id,
                      state='choose_button')
    bot.set_my_commands([
        telebot.types.BotCommand("/start", "Запуск бота")
    ])


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'catalog_types':
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

        bot.send_message(call.from_user.id, "Введите название прибора",
                         reply_markup=ReplyKeyboardRemove())
        storage.reset_data(chat_id=call.message.chat.id, user_id=call.from_user.id)

        storage.set_state(chat_id=call.message.chat.id, user_id=call.from_user.id, state='search')
        bot.answer_callback_query(callback_query_id=call.id, show_alert=True)
    elif call.data in keys2:
        bot.send_message(call.from_user.id, search_info(call.data))
        storage.reset_data(chat_id=call.message.chat.id, user_id=call.from_user.id)

        storage.set_state(chat_id=call.message.chat.id, user_id=call.from_user.id, state='search')
        bot.answer_callback_query(callback_query_id=call.id, show_alert=True)
    elif call.data == "menu":

        bot.send_message(call.from_user.id, "Привет! Нажми на кнопку, чтобы начать", reply_markup=gen_first_keyboard())
        storage.reset_data(chat_id=call.message.chat.id, user_id=call.from_user.id)

        storage.set_state(chat_id=call.message.chat.id, user_id=call.from_user.id, state='choose_button')
        bot.answer_callback_query(callback_query_id=call.id, show_alert=True)


@bot.message_handler(content_types=['text'])
def booking(message):
    print(message.text)
    match storage.get_state(chat_id=message.chat.id, user_id=message.from_user.id):
        case 'search':
            if (len(message.text) > 2):
                lis = list()
                s = message.text.lower
                main_keyboard = telebot.types.ReplyKeyboardMarkup()
                for i in range(0, len(keys3)):
                    if message.text.lower() in keys3[i].lower():
                        lis.append(keys2[i])
                if len(lis) == 0:
                    bot.send_message(message.chat.id, "Название не найдено", reply_markup=gen_search_keyboard(lis))
                else:
                    bot.send_message(message.chat.id, text=f"Найдено {len(lis)} совпадений",
                                     reply_markup=gen_search_keyboard(lis))
                    storage.set_state(chat_id=message.chat.id, user_id=message.from_user.id,
                                      state='search')

            else:
                bot.send_message(message.chat.id, "Название должно быть длинее 2 символов")

        case 'search_info':
            for item in keys2:
                if message.text.lower() in item.lower():
                    bot.send_message(message.chat.id, search_info(message.text))
                    storage.set_state(chat_id=message.chat.id, user_id=message.from_user.id,
                                      state='search')
                    storage.reset_data(chat_id=message.chat.id, user_id=message.from_user.id)
        case 'brand_type':
            if message.text in brands.keys():
                bot.send_message(message.chat.id, "Выбери название прибора",
                                 reply_markup=get_second_brand_keybord(message.text))
                storage.set_state(chat_id=message.chat.id, user_id=message.from_user.id,
                                  state='brand_name')
                storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                 key='brand_type', value=message.text)
            elif message.text == 'Меню':
                bot.send_message(message.chat.id, "Привет! Нажми на кнопку, чтобы начать",
                                 reply_markup=gen_first_keyboard())
                storage.reset_data(chat_id=message.chat.id, user_id=message.from_user.id)

                storage.set_state(chat_id=message.chat.id, user_id=message.from_user.id, state='choose_button')
            else:
                bot.send_message(message.chat.id, "Выберите бренд прибора")

        case 'brand_name':
            if (message.text in brands[
                storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['brand_type']].keys()):
                print(message.text)
                storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                 key='brand_name', value=message.text)
                bot.send_message(message.chat.id, get_info_brand(tg_id=message.chat.id))
            elif (message.text == '\U0001F519Назад'):
                bot.send_message(message.chat.id, "Выберите бренд прибора",
                                 reply_markup=get_brands_keyboard())
                storage.set_state(chat_id=message.chat.id, user_id=message.from_user.id,
                                  state='brand_type')
            else:
                bot.send_message(message.chat.id, "Название не найдено")
        case 'brand_info':
            print(1)
            if (message.text in brands[
                storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['brand_type']
                [storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['brand_name']]]):
                bot.send_message(message.chat.id, "Выбери  прибора",
                                 reply_markup=gen_second_keyboard(message.text))
                storage.set_state(chat_id=message.chat.id, user_id=message.from_user.id,
                                  state='choose_catalog_brand')
                storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                 key='catalog_brands', value=message.text)
            elif (message.text == '\U0001F519Назад'):
                bot.send_message(message.chat.id, "Выбери бренж прибора",
                                 reply_markup=gen_second_keyboard(
                                     storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)[
                                         'type']))
                storage.set_state(chat_id=message.chat.id, user_id=message.from_user.id,
                                  state='choose_brand')
            else:
                bot.send_message(message.chat.id, "Название не найдено. Поробуй еще раз")
        case 'choose_type':
            if (message.text in equipment_catalog.keys()):
                bot.send_message(message.chat.id, "Выбери бренд прибора",
                                 reply_markup=gen_second_keyboard(message.text))
                storage.set_state(chat_id=message.chat.id, user_id=message.from_user.id,
                                  state='choose_brand')
                storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                 key='type', value=message.text)
            elif (message.text == 'Меню'):
                bot.send_message(message.chat.id, "Привет! Нажми на кнопку, чтобы начать",
                                 reply_markup=gen_first_keyboard())
                storage.reset_data(chat_id=message.chat.id, user_id=message.from_user.id)

                storage.set_state(chat_id=message.chat.id, user_id=message.from_user.id, state='choose_button')
            else:
                bot.send_message(message.chat.id, "Ошибка. Поробуй еще раз")

        case 'choose_brand':
            if (message.text in equipment_catalog[
                storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['type']]):
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
            if (message.text in equipment_catalog[
                storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['type']]
            [storage.get_data(chat_id=message.chat.id, user_id=message.from_user.id)['brand']]):
                storage.set_state(chat_id=message.chat.id, user_id=message.from_user.id,
                                  state='choose_name')
                storage.set_data(chat_id=message.chat.id, user_id=message.from_user.id,
                                 key='name', value=message.text)
                bot.send_message(message.chat.id, get_info(message.from_user.id))
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
