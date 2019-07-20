from database import ActiveDatabase
from MatchClass import Match
from UserClass import User
from SensitiveConfig import *
from config import *
import requests
import time


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

def RateLimitFromHeader(limitCount):
    list = limitCount.split(',')
    current,limit = list[1].split(':',1)
    ratio = float(current)/float(limit)
    if ratio == .99:
        sleepTime = limit
    elif ratio == .75:
        sleepTime = 5
    else:
        sleepTime = 0

    if sleepTime:
        time.sleep(sleepTime)




def fetchMatchEntries(user):
    ''' fetches n number of matches from RiotGames api
    Args: dictionary
        region: "NA1"
        accountId: "6UoWroRfGgxqnI0Oj-KahipCC2TcQWiKkAar-BWyYGoxAw"
        summonerId: "afternoonview'
    Returns:
        TODO:
            check for rate limit on Riot's api   
    '''
    try:
        url = RIOT_FETCH_MATCHES_URL.format(user["region"], user["accountId"], RIOT_API_KEY, MAX_MATCH_FETCH)
        response = requests.get(url)
        if "X-App-Rate-Limit-Count" in response.headers:
            print(response.headers["X-App-Rate-Limit-Count"])
            RateLimitFromHeader(response.headers["X-App-Rate-Limit-Count"])
        matchList = response.json()['matches']
        success = True
    except Exception as e:
        print(e)
        matchList = None
        success = False
    
    return matchList, success

def fetchUsersInMatch(region,matchId):
    '''Attempts to retrieve match details
    Args:   region = NA1
            matchId = 38853692

    Returns: Dictionary of match details

    '''
    url = RIOT_FETCH_MATCH_DETAILS_URL.format(region,matchId,RIOT_API_KEY)
    print(url)
    response = requests.get(url)
    if "X-App-Rate-Limit-Count" in response.headers:
        print(response.headers["X-App-Rate-Limit-Count"])
        RateLimitFromHeader(response.headers["X-App-Rate-Limit-Count"])
    users = response.json()['participantIdentities']
    return users


def insertSingleMatch(match,account_id):
    '''Attempts to insert a match
    Args: dictionary of a Match class

    Returns: a response message 
    '''
    print("attempting to insert match")
    try:
        dbConnection = ActiveDatabase()
        matchConnection = dbConnection.getConn().collection(MATCHES)
        inMatchConnection = dbConnection.getConn().collection(IN_MATCH)
        doesExist = inMatchConnection.where(u'match_id',u'==',match['matchId']).where(u'personal_summoner_id',u'==',account_id).stream()
        for doc in doesExist:
            print (doc)
            print('Match already exists')
            return 'Exists'
        else:
            matchConnection.document(match['matchId']).set(match)
            print("inserting match")
            return 'Success'
    except Exception as e:
        print("An error has occured: {}".format(e))
        return 'Error'

def insertParticipant(participant,matchId,userAccountId):
    insertDict = dict()
    insertDict['match_id'] = matchId
    insertDict['summoner_id'] = participant
    insertDict['personal_summoner_id'] = userAccountId
    dbConnection = ActiveDatabase()
    inMatchConnection = dbConnection.getConn().collection(IN_MATCH)
    inMatchConnection.add(insertDict)

#TODO implement logger
def main():
    
    print("Running MatchFinder")

    userList, userListSuccess = fetchActiveUsers()
    if userListSuccess:
        for user in userList:
            print("Users successfully queried")
            #Changing connection into dictionary
            user = user.to_dict()
            #Creating User Class out of data received
            user = User(user['region'],user['summoner_id'],user['account_id'])
            matchList, matchListSuccess = fetchMatchEntries(user.toDict())
            if matchListSuccess:
                print("Matches successfully queried")
                for match in matchList:
                    match = Match(match['gameId'],match['timestamp'],user.getRegion())
                    
                    insertMatchMessage = insertSingleMatch(match.toDict(),user.getAccountId())
                    if insertMatchMessage is 'Success':
                        usersInMatch = fetchUsersInMatch(match.getRegion(),match.getMatchId())
                        for participant in usersInMatch:
                            insertParticipant(participant['player']['accountId'],match.getMatchId(),user.getAccountId())
                        print("need to query for match details")
                    elif insertMatchMessage is 'Exists':
                        print("Skipping user")
                        break
                    elif insertMatchMessage is 'Error':
                        print("Error should skip singular match")
            else:
                print("Failed to retrieve any active runs")
    else:
        print("Failed to retrieve any active users")

    #steps 
    #Get active users
    #for each active user
        #grab last 40 matches from riot api
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