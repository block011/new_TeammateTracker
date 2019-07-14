
#Current available regions
#The key points to the name that the api uses
ALL_REGIONS = {
    'BR':'br1',
    'EUN':'eun1',
    'EUW':'euw1',
    'JP':'jp1',
    'KR':'kr',
    'LA1':'la1',
    'LA2':'la2',
    'NA':'na1',
    'OC':'oc1',
    'TR':'tr1',
    'RU':'ru',
    'PBE':'pbe1'}

MATCH_FINDER_FILE_NAME = 'MatchFinder.py'
MATCH_FINDER_SCHEDULE_TIME = 10 # Minutes matchfinder waits before checking again


MAX_MATCH_FETCH = 50

#Args ---- Region, Accountid, apikey, max_games 
RIOT_FETCH_MATCH_URL = 'https://{}.api.riotgames.com/lol/match/v4/matchlists/by-account/{}?api_key={}&endIndex={}'

