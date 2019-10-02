import telebot
import time
import datetime as dt

class PlayersRecording:
    started = False

def fileInit():
    try:
        file = open(FILE_WITH_PLAYERS, 'r')
        file_dump = open(DUMP_FILE, 'r')
        file.close()
        file_dump.close()
    except:
        file = open(FILE_WITH_PLAYERS, 'a')
        file_dump = open(DUMP_FILE, 'a')
        file.close()
        file_dump.close()

def sayListWithNumbers(list):
    counter = 1
    resultText = ''
    for item in list:
        resultText += '{}. @{}\n'.format(counter, item)
        counter += 1
    return resultText

def sayList(list):
    resultText = ''
    for item in list:
        resultText += '{}\n'.format(item)
    return resultText

def getPlayersList():
    with open(FILE_WITH_PLAYERS, 'r') as file:
        str = file.read()
        if str:
            return str.split(',')
        else: return list()

def setPlayersList(players_list:list):
    with open(FILE_WITH_PLAYERS, 'w') as file:
        file.write(','.join(players_list))

def dumpResults():
    with open(DUMP_FILE, 'a') as dump_file:
        result_str = '[{}] '.format(dt.date.today()) + ','.join(getPlayersList()) + '\n'
        dump_file.write(result_str)
        setPlayersList([])

def getHist(lines: int = 5):
    with open(DUMP_FILE, 'r') as dump_file:
        history = dump_file.readlines()
        history.reverse()
        if len(history) < lines:
            return history
        else:
            short_history = []
            for i in range(lines):
                short_history.append(history[i])
            return short_history

FILE_WITH_PLAYERS = 'playersList.txt'
DUMP_FILE = 'dump.txt'

MY_TELEBOT = "887155034:AAHhLkSLS7Mkls2Go0TLSP0l2RFH4gvEVYI"

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

# сначала проверим есть ли рядом файл со списком игроков, если нет - создадим
fileInit()
# инициируем подключение к telegramm
bot = telebot.TeleBot(MY_TELEBOT)
# экземпляр класса где хрянятся свойства события
rec = PlayersRecording()
# playersList()

@bot.message_handler(commands=WORDS["START_COMMANDS"])
def start_message(message):
    if not rec.started:
        if getPlayersList():
            #print(message)
            bot.reply_to(message, "Продолжаем запись")
            rec.started = True
        else:
            #print(message)
            bot.reply_to(message, "Начинаем запись на ближайшую игру")
            rec.started = True
    else:
        bot.reply_to(message, "Запись уже ведется. Для записи на игру напишите '+', 'plus' или 'плюс'.\nДля завершения записи введите комманду /stop")

@bot.message_handler(commands=WORDS["STOP_COMMANDS"])
def stop_message(message):
    if rec.started:
        if getPlayersList():
            statusMessage = sayListWithNumbers(getPlayersList())
            bot.reply_to(message, "Запись на игру закончена. Список записавшихся:\n{}".format(statusMessage))
            dumpResults()
        else: bot.reply_to(message, "Никто не записался на ближайшую игру :( ленивые человеки...")
        rec.started = False
    else:
        bot.reply_to(message, "Запись ещё не началась. Для начала наберите комманду /start")

@bot.message_handler(commands=WORDS["STATUS_COMMANDS"])
def status_message(message):
    if rec.started:
        if getPlayersList():
            statusMessage = sayListWithNumbers(getPlayersList())
            bot.send_message(message.chat.id, 'Текущие записанные игроки:\n{}'.format(statusMessage))
        else: bot.reply_to(message, "Пока ещё никто не записался. Для записи напишите '+', 'plus' или 'плюс'")
    else:
        bot.reply_to(message, "Запись на ближайшую игру ещё не началась. Для начала наберите комманду /start")

@bot.message_handler(commands=['help'])
def status_message(message):
    bot.reply_to(message, HELP_DESCRIPTION)

@bot.message_handler(commands=['hist'])
def hist_message(message):
    history = getHist()
    if history:
        bot.reply_to(message, 'История записей:\n{}'.format(sayList(history)))
    else:
        bot.reply_to(message, 'Нет записей для отображения')

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if rec.started:
        if message.text in WORDS["PLUS_COMMANDS"]:
            if message.from_user.username not in getPlayersList():
                players_array = getPlayersList()
                players_array.append(message.from_user.username)
                setPlayersList(players_array)
                bot.reply_to(message, "Записал на следующую игру @{}.".format(message.from_user.username))
            else:
                bot.reply_to(message, "{} уже записан.".format(message.from_user.username))
        elif message.text in WORDS["MINUS_COMMANDS"]:
            if message.from_user.username in getPlayersList():
                players_array = getPlayersList()
                players_array.remove(message.from_user.username)
                setPlayersList(players_array)
                bot.reply_to(message, "@{}, ну и сиди дома, кожаный ублюдок".format(message.from_user.username))
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
        time.sleep(15)



# Текущий список команд для телеги
# start - Начать запись на ближайшую игру
# status - Посмотреть текущий список записавшихся
# stop - Закончить запись на ближайшую игру
# hist - Показать историю записей
# help - Бесполезная функция, которую никто никогда не использует

