from config import ALL_REGIONS

class Match:
    def __init__(self,id,creationTime,region):
        self.setMatchId(id)
        self.setGameCreated(creationTime)
        self.setRegion(region)

    def toDict(self):
        returnDict = dict()

        returnDict['matchId'] = self.getMatchId()
        returnDict['gameCreated'] = self.getGameCreated()
        returnDict['region'] = self.getRegion()

        return returnDict

    def getMatchId(self): 
        ''' Returns matchId '''
        return self.matchId
    
    def getGameCreated(self):
        ''' Returns gameCreated '''
        return self.gameCreated

    def getRegion(self):
        return self._region

    def setMatchId(self, id):
        ''' Sets matchId '''
        if str(id).isdigit():
            self.matchId = str(id)
        else:
            self.matchId = None
            raise Exception('matchId must be a digit')

    def setGameCreated(self, creationTime):
        ''' Sets gameCreated '''
        if str(creationTime).isdigit():
            self.gameCreated = str(creationTime)
        else:
            self.gameCreated = None
            raise Exception('gameCreated must be a digit')

    def setRegion(self, region):
    
        #Defaults region to None if region is invalid
        if region in ALL_REGIONS:
            self._region = ALL_REGIONS[region] 
        elif region in ALL_REGIONS.values():
            self._region = region
        else:
            _region = None
            raise Exception('Invalid region entered: {}'.format(region))
                



def main():
    print("Test for match class")
    matchTest = Match('382718461','19523452000','NA')
    print('match id : {} --- game created time : {}'.format(matchTest.getMatchId(), matchTest.getGameCreated()))

if __name__ == "__main__":
    main()

