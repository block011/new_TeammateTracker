from config import ALL_REGIONS

class User:#TODO Every time region is changed, update api path

    def __init__(self, region, summoner_id, account_id):
        
        self.setRegion(region) 
        self.setSummonerId(summoner_id)
        self.setAccountId(account_id)   

    def toDict(self):
        returnDict = dict()
        returnDict['region'] = self.getRegion()
        returnDict['summonerId'] = self.getSummonerId()
        returnDict['accountId'] = self.getAccountId()

        return returnDict


    def getRegion(self):
        return self._region

    def getSummonerId(self):
        return self._summonerId

    def getAccountId(self):
        return self._accountId

    def setRegion(self, region):
        
        #Defaults region to None if region is invalid
        if region in ALL_REGIONS:
            self._region = ALL_REGIONS[region] 
        elif region in ALL_REGIONS.values():
            self._region = region
        else:
            _region = None
            raise Exception('Invalid region entered: {}'.format(region))
            

    def setSummonerId(self, summoner_id):
        if summoner_id is not None or summoner_id != "":
            self._summonerId = summoner_id 
        else:
            _summonerId = None
            raise Exception('No id entered: {}'.format(summoner_id))

    def setAccountId(self, account_id):
        if account_id is not None or account_id != "":
            self._accountId = account_id
        else:
            self._accountId = None
            raise Exception(('no account id entered: {}'.format(account_id)))

def main():
    print("Test for user class")
    userTest = User("NA","Afternoonview","328fjrf429d32-423f-ewt23truh")
    print('summoner id : {} --- region : {}'.format(userTest.getSummonerId(), userTest.getRegion()))

if __name__ == "__main__":
    main()