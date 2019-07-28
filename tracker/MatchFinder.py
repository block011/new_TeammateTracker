from database import ActiveDatabase
from MatchClass import Match
from UserClass import User
from SensitiveConfig import *
from config import *
import requests
import time
import logging

logger = logging.getLogger(__name__)

def initLogger():
    logger.setLevel(logging.INFO)

    #Creating file handler
    handler = logging.FileHandler('{}/log/MatchFinder_{}.log'.format(CURRENT_FILE_PATH,time.strftime('%m%d_%H%M%S')))
    handler.setLevel(logging.INFO)

    #Creating logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    #add handlers to the logger
    logger.addHandler(handler)

def fetchActiveUsers():
    ''' fetches all active users
        Args: None

        Return:
            userList = dictionary of active users
            success = boolean on whether it grabbed users
    '''

    logger.info("Fetching active users")

    #accessing active database
    dbConnection = ActiveDatabase().getConn()
    userConnection= dbConnection.collection(USERS)
    try:
        userList = userConnection.stream()
        logger.info("Query was successful.")
        success = True
    except Exception as e:
        logger.warning("Exception was thrown!!! --- {}".format(e))
        userList = None
        success = False
    
    logger.info("Returning -- Success: {}".format(success))
    logger.info("          -- UserList: {}".format(success))
    return userList,success

def RateLimitFromHeader(limitCount):
    ''' Detects if script gets close to rate limit for api, then slows it down
        Args:
            limitCount = response.header["X-App-Rate-Limit-Count"]
        Return:
            None
    '''
    list = limitCount.split(',')
    current,limit = list[1].split(':',1)
    ratio = float(current)/float(limit)
    sleepTime = 0

    logger.info("Checking rate limit. current: {} limit: {} ratio: {}".format(current,limit,ratio))

    #Will need to be changed with producer key. Built for 120 rate limit every 2 minutes
    if ratio == .75:
        sleepTime = 2

    #Keeping this open for change, more distict sleep times may be added
    if sleepTime:
        time.sleep(sleepTime)

def fetchMatchEntries(user):
    ''' fetches n number of matches from RiotGames api
    Args: dictionary
        region: "NA1"
        accountId: "6UoWroRfGgxqnI0Oj-KahipCC2TcQWiKkAar-BWyYGoxAw"
        summonerId: "afternoonview'
    Returns:

    '''
    logger.info("Fetching match entries for user: {}".format(user["summonerId"]))

    try:
        url = RIOT_FETCH_MATCHES_URL.format(user["region"], user["accountId"], RIOT_API_KEY, MAX_MATCH_FETCH)
        logger.info("GET method: {}".format(url))
        response = requests.get(url)
        if response.status_code == 200:

            if "X-App-Rate-Limit-Count" in response.headers:
                RateLimitFromHeader(response.headers["X-App-Rate-Limit-Count"])
            matchList = response.json()['matches']
            success = True
        else:
            raise Exception("Invalid response code: {}".format(response.status_code))
    except Exception as e:
        logger.warning("Exception was thrown!!! --- {}".format(e))
        matchList = None
        success = False
    
    logger.info("Returning -- Success: {}".format(success))
    logger.info("          -- matchList: {}".format(matchList))
    return matchList, success

def fetchUsersInMatch(region,matchId):
    '''Attempts to retrieve match details
    Args:   region = NA1
            matchId = 38853692

    Returns: Dictionary of match details

    '''

    logger.info("Fetching summones from match: {}-{}".format(region,matchId))
    url = RIOT_FETCH_MATCH_DETAILS_URL.format(region,matchId,RIOT_API_KEY)
    logger.info("GET Method: ".format(url))

    response = requests.get(url)
    if "X-App-Rate-Limit-Count" in response.headers:
        RateLimitFromHeader(response.headers["X-App-Rate-Limit-Count"])
    users = response.json()['participantIdentities']

    logger.info("Returns -- users: {}".format(users))
    return users


def insertSingleMatch(match,account_id):
    '''Attempts to insert a match
    Args: dictionary of a Match class

    Returns: a response message 
    '''
    logger.info("Inserting single match into db")
    try:
        dbConnection = ActiveDatabase()
        matchConnection = dbConnection.getConn().collection(MATCHES)
        inMatchConnection = dbConnection.getConn().collection(IN_MATCH)
        logger.info("Checking if match exists")
        doesExist = inMatchConnection.where(u'match_id',u'==',match['matchId']).where(u'personal_summoner_id',u'==',account_id).stream()
        for doc in doesExist:
            logger.info("Match already exists")
            logger.info(doc)

            logger.info("Returns -- Exists")
            return 'Exists'
        else:
            matchConnection.document(match['matchId']).set(match)
            logger.info("Match not found!!!")
            logger.info("Attempting to insert match")

            logger.inf("Returns -- Success")
            return 'Success'
    except Exception as e:
        logger.info("An error has occured: {}".format(e))

        logger.info("Returns -- Error")
        return 'Error'

def insertParticipant(participant,matchId,userAccountId):
    ''' Inserts a document into the IN_MATCH database
        Args:
            participant = the participant's accountId
            matchId = current matchId
            userAccountId = the active user's personal accountId

    '''
    logger.info("Inserting participant: participant: {} matchId: {} userAccountId {}".format(participant,matchId,userAccountId))
    try:
        insertDict = dict()
        insertDict['match_id'] = matchId
        insertDict['summoner_id'] = participant
        insertDict['personal_summoner_id'] = userAccountId
        dbConnection = ActiveDatabase()
        inMatchConnection = dbConnection.getConn().collection(IN_MATCH)
        inMatchConnection.add(insertDict)

        logger.info("Successfully added participant")
    except Exception as e:
        logger.info("An error has occured: {}".format(e))


def main():
    logger.info("... Initializing MatchFinder ...")

    userList, userListSuccess = fetchActiveUsers()
    if userListSuccess:
        logger.info("Found users...")
        for user in userList:
            #Changing connection into dictionary
            user = user.to_dict()

            logger.info("Initializing run for user: {}".format(user))

            #Creating User Class out of data received
            user = User(user['region'],user['summoner_id'],user['account_id'])

            logger.info("Converted user into User class: {}".format(user.toDict()))

            matchList, matchListSuccess = fetchMatchEntries(user.toDict())
            if matchListSuccess:
                logger.info("Found matches...")
                for match in matchList:
                    match = Match(match['gameId'],match['timestamp'],user.getRegion())

                    logger.info("Initializing run for match: {}".format(match.toDict()))

                    insertMatchMessage = insertSingleMatch(match.toDict(),user.getAccountId())
                    if insertMatchMessage is 'Success':
                        usersInMatch = fetchUsersInMatch(match.getRegion(),match.getMatchId())
                        for participant in usersInMatch:
                            logger.info("Initializing participant: {}".format(participant['player']['accountId']))

                            insertParticipant(participant['player']['accountId'],match.getMatchId(),user.getAccountId())
                    elif insertMatchMessage is 'Exists':
                        logger.info("Match found that currently exists. Skipping user...")
                        break
                    elif insertMatchMessage is 'Error':
                        logger.info("Error has occured when inserting match. Skipping singular match...")
            else:
                logger.info("Failed to retrieve any active runs")
    else:
        logger.info("Failed to retrieve any active users")

if __name__ == "__main__":
    initLogger()
    main()