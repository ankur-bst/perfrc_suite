import subprocess as subp
import sys
import datetime
import logging
import json
import time
import os
from pywinauto.findwindows import find_window
from pywinauto.win32functions import SetForegroundWindow
import pyautogui

logging.basicConfig(filename=r"Logs\Logs.txt",level=logging.DEBUG)

def installBluestacks():
	#print("Installing Bluestacks")
	try:
		print("Opening json")
		with open('flags.json') as f:
			data = json.load(f)
		print("json opened")
		emuDir = os.path.join(os.getcwd(), "Emulator")
		list = os.listdir(emuDir)
		print(emuDir)
		print(list)
		print(len(list))
		for i in range(1,len(list)+1):
			print("Checking builds to test")
			flag = data["builds"][str(i)]["isFinished"]
			print(flag)
			if flag == 0:
				print("saving path")
				emupath = os.path.join(emuDir, data["builds"][str(i)]["filename"])
				print("emupath= " + str(emupath))
				break
			else:
				print("Data recorded for - " + str(data["builds"][str(i)]["filename"]))
				emupath = False
		if emupath:
			print("Installing...")
			proc_info = subp.Popen(emupath , shell=True)
			logging.info(str(datetime.datetime.now()) + " Starting BS4 Installer; filename = " + str(data["builds"][str(i)]["filename"]))
			#SetForegroundWindow(find_window(title='BlueStacks Installer'))
			#print("before click")
			time.sleep(7)
			pyautogui.click(683,533) #Intel Desktop Screen Co-ordinates
			#print("Install clicked at - " + str(pyautogui.position()))
			print("Please wait while Bluestacks gets installed")
			startTime = time.time()
			while proc_info.poll() is None:
				time.sleep(20)
			endTime = time.time()
			elapsedTime = endTime - startTime
			retCode = proc_info.returncode
			if retCode == 0:
				print("Bluestacks installed successfully in %s" % elapsedTime)
			else:
				print("Installation Failed")
			
		else:
			print("All emulators data recorded")
	except Exception as e:
		logging.info(str(datetime.datetime.now()) + " Couldn't find installer; exiting.. Error - " + str(e))
		print("exiting.. " + str(e))
		sys.exit(0)
#installBluestacks()