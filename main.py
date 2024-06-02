import telebot
from config import TOKEN, keys
from extensions import APIException, Converter


bot = telebot.TeleBot(TOKEN)



@bot.message_handler(commands=['start', 'help', ])
def start_message(message):
    text = ('This Bot can show you current currency price! \n'
'\n'
'To start working with it, you have to send message in format: \
<name of base currency> <name of currency which price you want to know> \
<amount of first currency> (decimal numbers must be separated with dot!)\n'
'\n'
    'To see the list of available currencies - write /values')
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Available currencies: '
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convertion(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')
        if len(values) != 3:
            raise APIException('Wrong quantity of parameters!')

        base, quote, amount = values
        res = Converter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f"User's error: \n {e}")
    except Exception as e:
        bot.reply_to(message, f'Failed to process your request. \n{e}')
    else:
        text = f'Price of {amount} {base} in {quote} is {res}'
        bot.reply_to(message, text)


bot.polling(none_stop=True)