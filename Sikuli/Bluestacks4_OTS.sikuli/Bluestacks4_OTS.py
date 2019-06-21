import logging
import datetime
import os, sys
import json

logging.basicConfig(filename=r"C:\Users\Administrator\Desktop\perf_rc_suite\Logs\Logs.txt",level=logging.DEBUG)

with open(r"C:\Users\Administrator\Desktop\perf_rc_suite\flags.json") as f:
    data = json.load(f)

curBuild = data["builds"]["current"]
isDefOTS = data["builds"][str(curBuild)]["defOTS"]

def slowType(text, time):
    for c in text:
        type(c)
        wait(time)
def OTS():
    try:
        if isDefOTS == 0:
            if exists("1552384923502.png", 60):
                click("1552384964986.png")
                logging.warning(str(datetime.datetime.now()) + " Clicked on Let's Go")
            else:
                logging.warning(str(datetime.datetime.now()) + " Couldnt find Let's Go")
        elif isDefOTS == 1:
            if exists("1558087631738.png", 60):
                click("1558087631738.png")
                logging.warning(str(datetime.datetime.now()) + " Clicked on sign in (def pop up)")
            else:
                logging.warning(str(datetime.datetime.now()) + " Couldnt find pop up sign in")
            if exists("1558085295209.png", 60):
                click("1558085295209.png")
                logging.warning(str(datetime.datetime.now()) + " Clicked on sign in (Play Store)")
            else:
                logging.warning(str(datetime.datetime.now()) + " Couldnt find Play Store sign in")
                

        if exists("1558085340140.png", 60):
            click("1558085340140.png")
            logging.warning(str(datetime.datetime.now()) + " Clicked on email field")
            wait(10)
            slowType("qatestblue", 1)
            logging.warning(str(datetime.datetime.now()) + " Typed in email")
            if exists("1558085375531.png", 30):
                click("1558085375531.png")
                logging.warning(str(datetime.datetime.now()) + " Clicked on Next")
            if exists("1558092315801.png", 30):
                click(Pattern("1558092315801.png").targetOffset(-305,3))
                logging.warning(str(datetime.datetime.now()) + " Clicked on Password field")
            wait(10)
            slowType("bluestacks", 1)
            logging.warning(str(datetime.datetime.now()) + " Typed in password")
            if exists("1558085375531.png", 30):
                click("1558085375531.png")
                logging.warning(str(datetime.datetime.now()) + " Clicked on Next")
            if exists("1558085468291.png", 30):
                click("1558085468291.png")
                logging.warning(str(datetime.datetime.now()) + " Clicked on I agree")
            if isDefOTS == 0:
                if exists("1551785052086.png", 30):
                    click("1551785062952.png")
                    logging.warning(str(datetime.datetime.now()) + " Clicked on Start Using Bluestacks")
            elif isDefOTS == 1:
                if exists(Pattern("1558087747659.png").targetOffset(447,234), 60):
                    click(Pattern("1558087747659.png").targetOffset(448,237))
                    logging.warning(str(datetime.datetime.now()) + " Clicked on arrow (backup page)")
                else:
                    logging.warning(str(datetime.datetime.now()) + " Couldnt find down arrow before accepting backup")
                if exists("1558087857165.png", 60):
                    click("1558087857165.png")
                    logging.warning(str(datetime.datetime.now()) + " Accepted Backup")
                else:
                    logging.warning(str(datetime.datetime.now()) + " Couldnt find Accept backup")
                    
                    
    except Exception, e:
        logging.warning(str(datetime.datetime.now()) + " Couldnt Complete OTS; error - " + str(e))
        sys.exit(0)

try:
    OTS()
except Exception, e:
    logging.warning(str(datetime.datetime.now()) + " Couldnt Complete OTS; error - " + str(e))