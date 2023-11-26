import telebot
import webbrowser
from encrypt import MessageEncrypter

bot = telebot.TeleBot("6580140065:AAH22nIckUWly1hiqd4sGjHJAswHc2yUQk0")
DEFAULT = 0
CAESAR = 1
VIGENERE = 2
stats = {}
log = {}


def InputBot(message, text):
    a = ''
    def ret(message):
        nonlocal a
        a = message.text
        return False

    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, ret)
    while not a:
        pass
    return a
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, я бот-шифрователь. \n Я могу зашифровать твое сообщение методом Цезаря или методом Виженера' +
                     '\n Введи /help, чтоюы узнать больше')

@bot.message_handler(commands=['help'])
def hlp(message):
    bot.send_message(message.chat.id, '/start - начать работу с ботом\n/help - описание команд\n/register - зарегистрировать пользователя' +
                     '\n/stats - получить статистику по пользователям\n/enc_caesar - зашифровать сообщение методом Цезаря' +
                     '\n/dec_caesar - расшифровать сообщение методом Цезаря \n /enc_vigenere - зашифровать сообщение методом Виженера' +
                     '\n/dec_vigenere - расшифровать сообщение методом Виженера\n /git - перейти на GitHub-страницу проекта' +
                     '\n /log - посмотреть журнал запросов для текущего пользователя\n /clear - очистить журнал запросов')


@bot.message_handler(commands=['register'])
def register(message):
    if message.from_user.username not in stats:
        stats[message.from_user.username] = 0
    bot.send_message(message.chat.id, 'Пользователь зарегистрирован')

@bot.message_handler(commands=['stats'])
def stats_(message):
    ans: str = 'Статистика по пользователям:'
    lst = [ans]
    for person, value in stats.items():
        lst.append(f'{person}: {value} запросов шифрования')
    bot.send_message(message.chat.id, '\n'.join(lst))


@bot.message_handler(commands=['enc_caesar'])
def c_encr(message):
    inpt = InputBot(message, "Введите данные для шифрования")
    inpt, key = inpt.split(' ')
    enc = MessageEncrypter(inpt)
    if message.from_user.username in stats:
        stats[message.from_user.username] += 1
    log[(inpt, key)] = enc.caesar_encrypt(int(key))
    bot.send_message(message.chat.id, log[(inpt, key)])

@bot.message_handler(commands=['dec_caesar'])
def c_decr(message):
    inpt = InputBot(message, "Введите данные для дешифрования")
    inpt, key = inpt.split(' ')
    enc = MessageEncrypter(inpt)
    if message.from_user.username in stats:
        stats[message.from_user.username] += 1
    log[(inpt, int(key))] = enc.caesar_decrypt(int(key))
    bot.send_message(message.chat.id, log[(inpt, int(key))])

@bot.message_handler(command=['enc_vigenere'])
def v_encr(message):
    inpt = InputBot(message, "Введите данные для шифрования")
    inpt, key = inpt.split(' ')
    enc = MessageEncrypter(inpt)
    if message.from_user.username in stats:
        stats[message.from_user.username] += 1
    log[(inpt, key)] = enc.vigenere_encrypt(key)
    bot.send_message(message.chat.id, log[(inpt, key)])

@bot.message_handler(command=['dec_vigenere'])
def v_encr(message):
    inpt = InputBot(message, "Введите данные для дешифрования")
    inpt, key = inpt.split(' ')
    enc = MessageEncrypter(inpt)
    if message.from_user.username in stats:
        stats[message.from_user.username] += 1
    log[(inpt, key)] = enc.vigenere_decrypt(key)
    bot.send_message(message.chat.id, log[(inpt, key)])

@bot.message_handler(command=['git'])
def git_(message):
    pass

@bot.message_handler(command=['log'])
def log_(message):
    s = []
    for key, val in log.items():
        s.append(f'{key} -> {val}')
    bot.send_message(message.chat.id, '\n'.join(s))

@bot.message_handler(command=['clear'])
def clear_(message):
    log.clear()


bot.infinity_polling()
