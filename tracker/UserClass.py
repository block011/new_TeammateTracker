
from config import *


class User:#TODO Every time region is changed, update api path

    def __init__(self, region, summoner_id):
        
        self.setRegion(region) 
        self.setSummonerId(summoner_id)   

    def getRegion(self):
        return self._region

    def getSummonerId(self):
        return self._summonerId

    def setRegion(self, region):
        
        #Defaults region to North America if region is invalid
        if region in ALL_REGIONS:
            self._region = ALL_REGIONS[region] 
        else:
            _region = None
            raise Exception('Invalid region entered: {}'.format(region))
            

    def setSummonerId(self, summoner_id):
        if summoner_id is not None:
            self._summonerId = summoner_id 
        else:
            _summonerId = None
            raise Exception('No id entered: {}'.format(summoner_id))


def main():
    print("Test for user class")
    userTest = User("NA","Afternoonview")
    print('summoner id : {} --- region : {}'.format(userTest.getSummonerId(), userTest.getRegion()))

if __name__ == "__main__":
    main()