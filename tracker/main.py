import schedule
import time
import os
from subprocess import Popen

from config import *
from SensitiveConfig import *


def runMatchFinder():       
    Popen('python {}/{}'.format(CURRENT_FILE_PATH,MATCH_FINDER_FILE_NAME))


#TODO: need to add logging mechanism
def main():
    
    schedule.every(10).minutes.do(runMatchFinder)

    while(True):
        try:
            schedule.run_pending()
            time.sleep(600) #Sleeping for 10 minutes 
        except KeyboardInterrupt:
            print("ManualBreak")
            break
        except:
            print("Uncaught error, continuing...")


if __name__ == "__main__":
    main()