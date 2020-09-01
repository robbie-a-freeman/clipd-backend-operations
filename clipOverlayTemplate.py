def loadFromFile(url):
    import pickle
    return pickle.load(open(url, 'rb'))


class ClipOverlayTemplate:

    team1 = None
    team2 = None
    score1 = None
    score2 = None
    currRound = None
    mapScore1 = None
    mapScore2 = None
    p1 = None
    p2 = None
    p3 = None
    p4 = None
    p5 = None
    p6 = None
    p7 = None
    p8 = None
    p9 = None
    p10 = None



    def __init__(self):
        print('Empty template initialized')
    
    class PlayerEntry:
        
        overlayObj = None
        alias = None
        health = None
        armor = None
        money = None
        killCount = None
        defuse = None
        w1 = None
        w2 = None
        nades = None
        deadSymbol = None

    def saveToFile(self, file):
        import pickle
        if file:
            pickle.dump(self, open(file, 'wb'))
        else:
            pickle.dump(self, open('save.test', 'wb'))
