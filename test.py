FILE_WITH_PLAYERS = 'test.txt'

class Game():
    started = False

def fileInit():
    try:
        file = open(FILE_WITH_PLAYERS, 'r')
        file.close()
    except:
        file = open(FILE_WITH_PLAYERS, 'a')
        file.close()

def getPlayersList():
    with open(FILE_WITH_PLAYERS, 'r') as file:
        str = file.read()
        if str:
            return str.split(',')
        else: list()

def setPlayersList(players_list):
    with open(FILE_WITH_PLAYERS, 'w') as file:
        file.write(','.join(players_list))


fileInit()
setPlayersList([])