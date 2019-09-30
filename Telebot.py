import telebot
import time

FILE_WITH_PLAYERS = 'playersList.txt'

class PlayersRecording:
    started = False

def fileInit():
    try:
        file = open(FILE_WITH_PLAYERS, 'r')
        file.close()
    except:
        file = open(FILE_WITH_PLAYERS, 'a')
        file.close()

def sayListWithNumbers(list):
    counter = 1
    resultText = ''
    for item in list:
        resultText += '{}. @{}\n'.format(counter, item)
        counter += 1
    return resultText

def playersList(player = None):
    if not hasattr(playersList, '_list'):
        playersList._list = list()
    if player:
        playersList._list.append(player)
    else: pass

def getPlayersList():
    with open(FILE_WITH_PLAYERS, 'r') as file:
        str = file.read()
        if str:
            return str.split(',')
        else: list()

def setPlayersList(players_list):
    with open(FILE_WITH_PLAYERS, 'w') as file:
        file.write(','.join(players_list))

MY_TELEBOT = "887155034:AAEtnT01OaazrM64zlTqwpKs29nLqsMHYNI"

# сначала проверим есть ли рядом файл со списком игроков, если нет - создадим
fileInit()
# инициируем подключение к telegramm
bot = telebot.TeleBot(MY_TELEBOT)

HELP_DESCRIPTION = """
Коротко: описание доступных комманд есть в опциях бота.
Процесс формирования комманды: 
    1. Начинаем запись коммандой /start
    2. Записываемся с помощью слов '+', 'plus', 'плюс'
    3. Удаляем запись с помощью слов '-', 'minus', 'minus' (осторожно, он ругается)
    3 с половиной. Если надо, проверяем текущий список игроков коммандой /status
    4. Заканчиваем запись коммандой /stop
"""

WORDS = {    "START_COMMANDS":  ['start']
            ,"STOP_COMMANDS":   ['stop']
            ,"STATUS_COMMANDS": ['status']
            ,"PLUS_COMMANDS":   ['+', 'plus', 'плюс']
            ,"MINUS_COMMANDS":  ['-', 'minus', 'minus']}

rec = PlayersRecording()
playersList()

@bot.message_handler(commands=WORDS["START_COMMANDS"])
def start_message(message):
    if not rec.started:
        print(message)
        playersList._list = []
        bot.reply_to(message, "Начинаем запись на ближайшую игру")
        rec.started = True
    else:
        bot.reply_to(message, "Запись уже ведется. Для записи на игру напишите '+', 'plus' или 'плюс'.\nДля завершения записи введите комманду /stop")

@bot.message_handler(commands=WORDS["STOP_COMMANDS"])
def stop_message(message):
    if rec.started:
        if playersList._list:
            statusMessage = sayListWithNumbers(playersList._list)
            bot.reply_to(message, "Запись на игру закончена. Список записавшихся:\n{}".format(statusMessage))
        else: bot.reply_to(message, "Никто не записался на ближайшую игру :( ленивые человеки...")
        rec.started = False
    else:
        bot.reply_to(message, "Запись ещё не началась. Для начала наберите комманду /start")

@bot.message_handler(commands=WORDS["STATUS_COMMANDS"])
def status_message(message):
    if rec.started:
        if playersList._list:
            statusMessage = sayListWithNumbers(playersList._list)
            bot.send_message(message.chat.id, 'Текущие записанные игроки:\n{}'.format(statusMessage))
        else: bot.reply_to(message, "Пока ещё никто не записался. Для записи напишите '+', 'plus' или 'плюс'")
    else:
        bot.reply_to(message, "Запись на ближайшую игру ещё не началась. Для начала наберите комманду /start")

@bot.message_handler(commands=['help'])
def status_message(message):
    bot.reply_to(message, HELP_DESCRIPTION)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    #print(startedState._bool)
    if rec.started:
        if message.text in WORDS["PLUS_COMMANDS"]:
            if message.from_user.username not in playersList._list:
                playersList(message.from_user.username)
                bot.reply_to(message, "Записал на следующую игру @{}.".format(message.from_user.username))
            else:
                bot.reply_to(message, "{} уже записан.".format(message.from_user.username))
        elif message.text in WORDS["MINUS_COMMANDS"]:
            if message.from_user.username in playersList._list:
                playersList._list.remove(message.from_user.username)
                bot.reply_to(message, "Ну и сиди дома, кожаный ублюдок")
            else:
                bot.reply_to(message, "@{} пока ещё нет в списке. Сначала запишись, написав в чат '+', 'plus' или 'плюс'".format(message.from_user.username))
    else:
        if message.text in WORDS["PLUS_COMMANDS"] + WORDS["MINUS_COMMANDS"]:
            bot.reply_to(message, "Запись на ближайшую игру ещё не началась. Для начала наберите комманду /start")
        else: pass

# bot.reply_to(message, "{} уже записан.".format(message.from_user.username))

while True:
    try:
        bot.polling()
    except Exception as e:
        print(e)
        time.sleep(5)


# Текущий список команд для телеги
# start - Начать запись на ближайшую игру
# status - Посмотреть текущий список записавшихся
# stop - Закончить запись на ближайшую игру
# help - Бесполезная функция, которую никто никогда не

