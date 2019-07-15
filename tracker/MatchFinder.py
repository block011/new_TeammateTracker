from database import ActiveDatabase
from MatchClass import Match
from UserClass import User
from SensitiveConfig import *
from config import *
import requests


def fetchActiveUsers():
    ''' fetches all active users'''
    #accessing active database
    dbConnection = ActiveDatabase().getConn()
    userConnection= dbConnection.collection(u'users')
    try:
        userList = userConnection.stream()
        success = True
    except Exception as e:
        print(e)
        userList = None
        success = False
    
    return userList,success

def fetchMatchEntries(user):
    ''' fetches n number of matches from RiotGames api
    Args: dictionary
        region: "NA1"
        accountId: "6UoWroRfGgxqnI0Oj-KahipCC2TcQWiKkAar-BWyYGoxAw"
        summonerId: "afternoonview'
    Returns:
        TODO:   
    '''
    try:
        url = RIOT_FETCH_MATCH_URL.format(user["region"], user["accountId"], RIOT_API_KEY, MAX_MATCH_FETCH)
        response = requests.get(url).json()
        matchList = response['matches']
        success = True
    except Exception as e:
        print(e)
        matchList = None
        success = False
    
    return matchList, success

    def insertSingleMatch(match):
    '''Attempts to insert a match
    Arg: dictionary of Match

    Returns: a response message 

    '''
    print("attempting to insert match")
    try:
        dbConnection = ActiveDatabase().getConn()
        matchConnection = dbConnection.collection(MATCHES)

        matchConnection.document(match['matchId']).set(match)

        return True

    except Exception as e:
        print(e)

        return False
    #TODO
    #success
    #accessed database but id was taken
    #could not access database

#TODO implement logger
def main():
    
    print("Running MatchFinder")

    userList, userListSuccess = fetchActiveUsers()
    if userListSuccess:
        for user in userList:
            print("Users successfully queried")
            user = user.to_dict()
            user = User(user['region'],user['summoner_id'],user['account_id'])
            matchList, matchListSuccess = fetchMatchEntries(user.toDict())
            if matchListSuccess:
                print("Matches successfully queried")
                for match in matchList:
                    match = Match(match['gameId'],match['timestamp']).toDict()
                    
                    insertMatchSuccess = insertSingleMatch(match)
                    if insertMatchSuccess:
                        print("need to query for match details")
                    else:
                        print("Match failed skipping user")
                        break
            else:
                print("Failed to retrieve any active runs")
    else:
        print("Failed to retrieve any active users")

    #steps 
    #Get active users
    #for each active user
        #grab last 100 matches from riot api
        #for each match
            #if match does not exists in our database
                #add the match
                #for each summoner in match
                    #add summoner
                    #add summoner_in_match
            #else 
                #break




if __name__ == "__main__":
    main()