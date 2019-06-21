import logging

logging.basicConfig(filename=r"C:\Users\Administrator\Desktop\Perf RC Automation\Logs\Logs.txt",level=logging.DEBUG)

try:
    if exists("1551424231628.png", 60): 
        click("1551424251627.png")
    if exists("1551424399303.png", 200):
        click("1551424433302.png")
except Exception, e:
    logging.warning(str(datetime.datetime.now()) + " Couldnt Complete Installation; error - " + e)