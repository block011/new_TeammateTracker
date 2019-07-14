from database import ActiveDatabase
from MatchClass import Match
from UserClass import User
from SensitiveConfig import *
from config import *
import requests


def fetchMatchEntries(user):
    ''' fetched n number of matches from RiotGames api
    Args: dictionary
        region: "NA1"
        accountId: "6UoWroRfGgxqnI0Oj-KahipCC2TcQWiKkAar-BWyYGoxAw"
        summonerId: "afternoonview'
    Returns:
        TODO:   
    '''

    url = RIOT_FETCH_MATCH_URL.format(user["region"], user["accountId"], RIOT_API_KEY, MAX_MATCH_FETCH)
    print(url)
    response = requests.get(url).json()
    for match in response['matches']:
        print (match)
    return True,True

#TODO implement logger
def main():
    
    print("Running MatchFinder")

    #accessing active database
    dbConnection = ActiveDatabase().getConn()
    userConnection= dbConnection.collection(u'users')
    try:
        userList = userConnection.stream()
    except Exception as e:
        print(e)
        userList = None

    for user in userList:
        user = user.to_dict()
        user = User(user['region'],user['summoner_id'],user['account_id'])
        matchList, matchListSuccess = fetchMatchEntries(user.toDict())

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