import telebot
from telebot import types
import logging
bot = telebot.TeleBot("token")
value_b = 0
value_a = 0
res = 0
cho = ''
comp = ''

logging.basicConfig(level=logging.INFO, filename="log.log", filemode="a+",
                    format="%(asctime)s %(message)s")


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/reg':
        mrk = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key1 = types.KeyboardButton('Рациональные')
        key2 = types.KeyboardButton('Комплексные')
        mrk.add(key1, key2)
        bot.send_message(
            message.chat.id, f'Калькулятор \nСделайте выбор, с какими числами работать', reply_markup=mrk)
        bot.register_next_step_handler(message, choose)
    else:
        logging.info(
            f'user: {message.from_user.first_name} nickname: {message.from_user.username} : {message.text}')
        bot.send_message(message.from_user.id, 'Напиши /reg')


def choose(message):
    global comp
    comp = message.text
    bot.send_message(message.from_user.id, 'Введите первую цифру: ')
    bot.register_next_step_handler(message, val_a)


def val_a(message):
    global value_a
    if comp == "Рациональные":
        value_a = int(message.text)
    else:
        value_a = complex(message.text)
    button_click(message)


def button_click(message):
    global cho
    global comp
    mrk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    key1 = types.KeyboardButton('+')
    key2 = types.KeyboardButton('-')
    key3 = types.KeyboardButton('*')
    key4 = types.KeyboardButton('/')
    key5 = types.KeyboardButton('//')
    key6 = types.KeyboardButton('%')
    if comp == "Рациональные":
        mrk.add(key1, key2, key3, key4, key5, key6)
    else:
        mrk.add(key1, key2, key3, key4)
    bot.send_message(message.chat.id, 'Выберите операцию', reply_markup=mrk)
    bot.register_next_step_handler(message, cho_init)


def cho_init(message):
    global cho
    cho = str(message.text)
    bot.send_message(message.chat.id, 'Введите вторую цифру:')
    bot.register_next_step_handler(message, controller)


def controller(message):
    global res
    global value_a
    global value_b
    global cho
    global comp
    if comp == "Рациональные":
        value_b = int(message.text)
    else:
        value_b = complex(message.text)
    if cho == "+":
        res = value_a + value_b
    elif cho == "-":
        res = value_a-value_b
    elif cho == "*":
        res = value_a*value_b
    elif cho == "/":
        res = value_a/value_b
    elif cho == "//":
        res = value_a//value_b
    elif message.text == "%":
        res = value_a % value_b

    bot.send_message(message.chat.id, f'{value_a} {cho} {value_b} = {res}')

    logging.info(
        f'user: {message.from_user.first_name} nickname: {message.from_user.username} : {value_a} {cho} {value_b} {res}')


bot.polling(none_stop=True, interval=0)
