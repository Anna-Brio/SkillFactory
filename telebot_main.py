import telebot
from telebot_config import keys, TOKEN
from extentions import ConversionException, CryptoConvertor

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = "Чтобы начать работу, введите команду боту в следующем формате:\n <имя валюты> \
    <в какую валюту перевести> \
    <количество переводимой валюты> \nУвидеть список всех доступных валют: /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступнте Валюты:"
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message): # биткоин доллар 1
    try:
        params = message.text.split(' ')

        if len(params) != 3:
            raise ConversionException("Too many or too few parameters.")

        quote, base, amount = params
        total_base = CryptoConvertor.get_price(quote, base, amount)

    except ConversionException as e:
        bot.reply_to(message, f"Input error: \n{e}")
    except Exception as e:
        bot.reply_to(message, f'Convertion failed \n{e}')
    else:
        # text = f'Цена {amount} {quote} в {base} - {total_base}'
        text = f'The price of {amount} {quote} in {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()

