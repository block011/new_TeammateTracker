from ../resources/config import *

class Match:
    def __init__(self,id,creationTime):
        self.setMatchId(id)
        self.setGameCreated(creationTime)

    def getMatchId(self):
        return self.matchId
    
    def getGameCreated(self):
        return self.gameCreated

    def setMatchId(self, id):
        if id.isdigit():
            self.matchId = id
        else:
            self.matchId = None
            raise Exception('matchId must be a digit')

    def setGameCreated(self, creationTime):
        if creationTime.isdigit():
            self.gameCreated = creationTime
        else:
            self.gameCreated = None
            raise Exception('gameCreated must be a digit')


def main():
    print("Test for match class")
    matchTest = Match('382718461','19523452000')
    print('match id : {} --- game created time : {}'.format(matchTest.getMatchId(), matchTest.getGameCreated()))

if __name__ == "__main__":
    main()

