import subprocess as subp
import logging
import datetime

logging.basicConfig(filename=r".\..\Logs\Logs.txt",level=logging.DEBUG)

def runSikuli(script):
	if script == 0:
		logging.info(str(datetime.datetime.now()) + " Starting OTS")
		subp.call(r'C:\Users\Administrator\Desktop\perf_rc_suite\Sikuli\runsikulix.cmd -r C:\Users\Administrator\Desktop\perf_rc_suite\Sikuli\Bluestacks4_OTS.sikuli')
		#return True
	elif script == 1:
		logging.info(str(datetime.datetime.now()) + " Exiting Bluestacks")
		subp.call(r'C:\Users\Administrator\Desktop\perf_rc_suite\Sikuli\runsikulix.cmd -r C:\Users\Administrator\Desktop\perf_rc_suite\Sikuli\quitBluestacks.sikuli')
	else:
		print("Wrong parameter given")