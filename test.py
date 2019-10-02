FILE_WITH_PLAYERS = 'test.txt'
DUMP_FILE = 'dump.txt'

class Game():
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
        result_str = ','.join(getPlayersList()) + '\n'
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

print(showHist(5))
