import schedule
import time
import os
from subprocess import Popen

from SensitiveConfig import CURRENT_FILE_PATH 
from config import MATCH_FINDER_FILE_NAME,  MATCH_FINDER_SCHEDULE_TIME

def runMatchFinder():       
    Popen('python {}/{}'.format(CURRENT_FILE_PATH,MATCH_FINDER_FILE_NAME))


#TODO: need to add logging mechanism
def main():
    
    schedule.every(MATCH_FINDER_SCHEDULE_TIME).minutes.do(runMatchFinder)

    while(True):
        try:
            schedule.run_pending()
            time.sleep(60) #Sleeping for 1 minute(s)
        except KeyboardInterrupt:
            print("ManualBreak")
            break
        except:
            print("Uncaught error, continuing...")


if __name__ == "__main__":
    main()