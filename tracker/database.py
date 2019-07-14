import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from config import *

#Parent database class -- established connection using firebase json
class SuperDatabase:
    def __init__(self,firebaseConnection):
        self.cred = credentials.Certificate(firebaseConnection)
        firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()

#Singletone
#Creates a SuperDatabase using LEAGUE_DATABASE_JSON
class LeagueDatabase:
    #Singleton instance
    instance = None
    class __LeagueDatabase(SuperDatabase):
        def __init__(self, baseCollection):
            SuperDatabase.__init__(self, LEAGUE_DATABASE_JSON)
            self.__setBaseConn__(baseCollection)

        def __getBaseConn__(self):
            return self.__conn 

        def __setBaseConn__(self, baseCollection):
            self.__conn = self.db.collection(baseCollection)

    def __init__(self, baseCollection):
        if not LeagueDatabase.instance:
            LeagueDatabase.instance = LeagueDatabase.__LeagueDatabase(baseCollection)
        else:
            LeagueDatabase.instance.__setBaseConn__(baseCollection)

    #get instance
    def getInstance(self):
        return LeagueDatabase.instance
   

#Uses LeagueDatabase to access the active db
class ActiveDatabase(LeagueDatabase):
    def __init__(self):
        try:
            LeagueDatabase.__init__(self, BASE_COLLECTION_NAME)
            self.__conn = self.getInstance().__getBaseConn__().document(ACTIVE_DB_NAME)
        except:
            self.__conn = None
            raise('Error Connecting to Firebase')
 
    def getConn(self):
        return self.__conn

#Uses LeagueDatabase to access the active db
class ArchiveDatabase(LeagueDatabase):
    def __init__(self):
        try:
            LeagueDatabase.__init__(self, BASE_COLLECTION_NAME)
            self.__conn = self.getInstance().__getBaseConn__().document(ARCHIVE_DB_NAME)
        except:
            self.__conn = None
            raise('Error connecting to Firebase')
    def getConn(self):
        return self.__conn

