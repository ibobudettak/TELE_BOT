import telebot
from Token_tele_bot import TELE_TOKEN
import Parser

bot = telebot.TeleBot(TELE_TOKEN)
TO_CHAT_ID = 965904484

keyboard_menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_button_1 = telebot.types.InlineKeyboardButton('Каталог', callback_data='Каталог')
keyboard_button_2 = telebot.types.InlineKeyboardButton('Контакты', callback_data='Контакты')
keyboard_button_3 = telebot.types.InlineKeyboardButton('Доставка и оплата', callback_data='Доставка и оплата')
keyboard_button_4 = telebot.types.InlineKeyboardButton('Обратная связь', callback_data='Обратная связь')

keyboard_menu.add(keyboard_button_2, keyboard_button_1, keyboard_button_3, keyboard_button_4)

keyboard_1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_1.row('Ведро', 'Вешалка', 'Горшок', 'Совок')
keyboard_1.row('Кактусница', 'Кашпо', 'Коврик')
keyboard_1.row('Контейнер', 'Кружка', 'Лейка')
keyboard_1.row('Мыльница', 'Плечики', 'Полка для обуви')
keyboard_1.row('Мыльница', 'Сушилка', 'Таз', 'Ящик')
keyboard_1.row('Главное меню')

list_keyboard_1 = ['Ведро', 'Вешалка', 'Горшок', 'Совок', 'Кактусница', 'Кашпо', 'Коврик', 'Контейнер', 'Кружка',
                   'Лейка', 'Мыльница', 'Плечики', 'Полка для обуви', 'Мыльница', 'Сушилка', 'Таз', 'Ящик']


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'ПТК "Домашние Мелочи" - производство товаров народного потребления. '
                                      'Мы рады приветствовать вас в нашем боте! ', reply_markup=keyboard_menu)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text in list_keyboard_1:
        selection = f"""SELECT * FROM goods WHERE Наименование LIKE '%{message.text}%' ORDER BY Цена ASC """
        if len(Parser.bot_output(selection=selection)) > 4096:
            for x in range(0, len(Parser.bot_output(selection=selection)), 4096):
                bot.send_message(message.chat.id, f'{Parser.bot_output(selection=selection)[x:x + 4096]}')
        else:
            for i in Parser.bot_output(selection=selection):
                bot.send_message(message.chat.id, f'{i}')

    elif message.text == 'Каталог':
        bot.send_message(message.chat.id, '*** Домашние мелочи *** ', reply_markup=keyboard_1)

    elif message.text == 'Доставка и оплата':
        bot.send_message(message.chat.id, '********  Доставка и оплата  ********\n\n' + '''Минимальная сумма отгрузки в 
        регионы составляет 20 000 рублей, для Омских
        покупателей – 5 000 рублей.
         
*************  Доставка  *************
        
        Мы организуем доставку нашего товара до склада партнеров как своим, так и наемным транспортом.
        Как правило, Вы получаете заказ в течение недели.
        Исключение составляют сезонные товары, которые не всегда имеются на складе в достаточном количестве и товары, 
        реализуемые в рамках акций, спецпредложений и производимые под заказ определенного клиента.
        Сроки и стоимость доставки определяются индивидуально и зависят от суммы и ассортимента заказа.
        Мы доставляем нашу продукцию по всей территории России и ближнего зарубежья.
        
**************  Оплата  **************
        
        Мы работаем по предоплате. Если Вы являетесь новым клиентом, то её размер составит для Вас 100%.
        В дальнейшем возможна частичная отсрочка платежа; размер и сроки будут зависеть от сложившихся между нами 
        отношений. Цены на продукцию указаны оптовые базовые. 
        Размер скидки индивидуален и зависит от объёма заказа и способа оплаты. 
        При заказе крупных товарных партий или партий товара СТМ предусмотрены индивидуальные условия сотрудничества.
        В случае если у Вас возникли вопросы при оформлении заказа, Вы всегда можете обратиться в наш отдел продаж по
        телефонам  +7 381 248-01-33, +7 904 077-53-48''' + '\n\n**************************************')

    elif message.text == 'Главное меню':
        bot.send_message(message.chat.id, '*** Домашние мелочи *** ', reply_markup=keyboard_menu)

    elif message.text == 'Контакты':
        bot.send_message(message.chat.id, '************  Наш адрес  ************\n\n'+'''РФ, г.Омск, ул. Омская, 213/1\n 
        Время работы: пн-пт 9:00-17:30\nОтдел оптовых продаж: +7 (3812) 95-63-90, +7 904 077-53-48\n
        Региональный отдел: +7 908 109-30-88\nОтдел закупа: +7 904 077-53-58\n
        Производственный отдел: +7 913 988-21-79\ne-mail: tkdm@mail.ru (по общим вопросам)\n
        e-mail: web.tkdm@mail.ru (по сотрудничеству и работе с регионами) \nSkype: omsk-tkdm\n'''+'\n******************'
                                                                                                  '*******************')

    elif message.text == 'Обратная связь':
        bot.send_message(message.from_user.id, "введите номер телефона!")
        bot.register_next_step_handler(message, get_num)

    else:
        bot.send_message(message.chat.id, '☺')


phone_number = None
client_name = None


def get_num(message):
    global phone_number
    phone_number = message.text
    bot.send_message(message.from_user.id, "Введите Ваше имя!")
    bot.register_next_step_handler(message, get_name)


def get_name(message):
    global client_name
    client_name = message.text
    bot.send_message(message.from_user.id, f"Данные приняты: Имя {client_name}, тел. {phone_number}!")
    bot.send_message(chat_id=TO_CHAT_ID, text=f'Клиент ждет звонка: Имя {client_name}, тел. {phone_number}!')


bot.polling(none_stop=True)
