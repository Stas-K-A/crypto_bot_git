import telebot
from config import keys, TOKEN
from extensions import CryptoConverter, ConvertionException


#создаем телеграмм-бота
#конвертирует валютные пары из предложенного списка, в том числе криптовалюты
bot = telebot.TeleBot(TOKEN)


#обработка ботом команд
@bot.message_handler(commands = ['start', 'help'])
def help(message):
    
    #текст с правилами работы для вывода в консоль бота
    text = 'Запрос обменного курса валютных пар в формате:\n\n\
<Валюта №1> <Валюта №2> <Количество валюты №1>\n\
Список всех доступных для обмена валют: /values'
    
    bot.reply_to(message, text)


#обработка ботом команд
@bot.message_handler(commands = ['values'])
def values(message):

    text = 'Список доступных для обмена валют:\n\n' + "\n".join(keys)
    bot.reply_to(message, text)


#обработка ботом текстовых сообщений
@bot.message_handler(content_types = ['text', ])
def convert(message):
    
    try:
        #строка сообщения, введенная пользователем в консоле бота
        #преобразуеv в список
        values = message.text.split()

        if len(values) != 3:
        #проверка количества параметров в текстовом сообщении - 3
        #1 - название валюты №1
        #2 - название валюты №2
        #3 - количество валюты №1
            raise ConvertionException(f'Количество параметров должно быть равно'
                                      f' - 3\n')

        val_1, val_2, count_val_1  = values
        #преобразование названий валлют в нижний регистр
        val_1 = val_1.lower()
        val_2 = val_2.lower()
        
        #получение обменного курса с помощью метода convert класса CryptoConvert
        price_val_1 = CryptoConverter.get_price(val_1, val_2, count_val_1)

    except ConvertionException as e:
        #вывод сообщений об ошибках ввода в консоль бота
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    
    except Exception as e:
        #вывод сообщений о системных ошибках в консоль бота
        bot.reply_to(message, f'Не получается обработать команду\n{e}')
    
    else:
        #вывод обменного курса установленной пользователем валютной пары
        #в консоль бота
        text = f'Стоимость {count_val_1} {val_1} в {val_2} - {price_val_1}'
        bot.send_message(message.chat.id, text)


bot.polling(non_stop = True)#запуск бота @Crypto_Trabaja_Bot
