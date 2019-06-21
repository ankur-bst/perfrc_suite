import subprocess
import time
import psutil
import os
import logging
import datetime
import launchemulator

logging.basicConfig(filename=os.path.join(os.getcwd(),"Logs\Logs.txt"),level=logging.DEBUG)


def startCollect(num, dir):
	try:
		#os.chdir(r'C:\Users\Administrator\Desktop\perf_rc_suite\PyScripts')
		curdir = os.getcwd()
		newpath =  curdir + '\\Results\\' + str(dir) + '\\PerfViewData\\'
		if not os.path.exists(newpath):
			print(newpath)
			os.makedirs(newpath)
			logging.info(str(datetime.datetime.now()) + " Creating directory for perfview data; path = " + str(dir))
	except Exception as e:
		print("Couldn't create directory; Error - " + str(e))
		logging.warning(str(datetime.datetime.now()) + " Couldn't create directory; Error - " + str(e))
	try:
		logging.info(str(datetime.datetime.now()) + " Starting PerfView")
		subprocess.Popen(r'.\PyScripts\Perfview.exe /NoView /NoGUI collect .\\Results\\' + str(dir) +  '\\PerfViewData\\'+str(num)+'.PerfViewData.etl', shell=True) 	
	except Exception as e:
		print("Couldn't start PerfView - " + str(e))
		
def stopCollect(num, dir):
	print(os.getcwd())
	try:
		#os.chdir(r'C:\Users\Administrator\Desktop\perf_rc_suite\PyScripts')
		print('Stopping Perfview')
		logging.info(str(datetime.datetime.now()) + " Stopping PerfView")
		stop = subprocess.Popen(r'Perfview stop', shell=True)	
	#	time.sleep(300)
	except Exception as e:
		print("Couldn't stop PerfView - " + str(e))
		logging.info(str(datetime.datetime.now()) + " Couldn't stop PerfView - " + str(e))
	try:
		while True:
			if os.path.exists(os.path.join(os.getcwd(),'Results',str(dir),'PerfViewData',str(num)+'.PerfViewData.etl.zip')):
				logging.info(str(datetime.datetime.now()) + " PerfView data merge completed")
				print('found')
				break
			else:
				print('sleep')
				time.sleep(5)
	except Exception as e:
		print("Couldn't find .etl file - " + str(e))
		logging.info(str(datetime.datetime.now()) + " Couldn't find .etl file - " + str(e))
				
def killPerfView():
	try:
		print('Killing Perfview')
		logging.info(str(datetime.datetime.now()) + " Killing PerfView")
		for proc in psutil.process_iter():
			if proc.name() == "PerfView.exe":
				proc.kill()
	except Exception as e:
		print("Couldn't kill PerfView - " + str(e))
		logging.info(str(datetime.datetime.now()) + " Couldn't Kill PerfView")

#startCollect(2, 'SubBootPerf')
#stopCollect(1)
#killPerfView()	