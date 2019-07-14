import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import SensitiveConfig as sc

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
            SuperDatabase.__init__(self, sc.LEAGUE_DATABASE_JSON)
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
            LeagueDatabase.__init__(self, sc.BASE_COLLECTION_NAME)
            self.__conn = self.getInstance().__getBaseConn__().document(sc.ACTIVE_DB_NAME)
        except Exception as e:
            self.__conn = None
            raise e
 
    def getConn(self):
        return self.__conn

#Uses LeagueDatabase to access the active db
class ArchiveDatabase(LeagueDatabase):
    def __init__(self):
        try:
            LeagueDatabase.__init__(self, sc.BASE_COLLECTION_NAME)
            self.__conn = self.getInstance().__getBaseConn__().document(sc.ARCHIVE_DB_NAME)
        except Exception as e:
            self.__conn = None
            raise e
    def getConn(self):
        return self.__conn


def main():
    try:
        test1 = ActiveDatabase()
        test2 = ArchiveDatabase()
        print("Success")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()