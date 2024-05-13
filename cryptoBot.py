import telebot
from config import keys, TOKEN
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = (f'Привет, {message.from_user.first_name}!\nЕсли нужна помощь, переходи по ссылке: /help')
    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = ('Чтобы начать работу, введи команду в следующем формате:(Имя валюты необходимо указать '
            'без склонения)\n1.Имя валюты (например: Рубль, Евро, Доллар)\
    \n2.В какую валюту перевести (например: Рубль, Евро, Доллар)\n3.Колличество переводимой валюты (сколько?)'
            '\n-Увидеть список доступной валюты возможно по ссылке: /values')
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступная валюта:'
    for key in keys.keys():
        text = '\n'.join((text,key,))
    bot.reply_to(message,text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')

        if len(values) != 3:
           raise APIException ('Я не понимаю эти параметры! Следуй инструкции /help.')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена: {amount} {quote} в {base} = {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(non_stop=True)