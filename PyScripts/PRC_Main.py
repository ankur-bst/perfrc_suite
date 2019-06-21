import PRC_Boot
import PRC_CPU_RAM
import restart_machine
import stable_cpu
import time
import json
import sikuliController
import BluestacksUninstall
import launchinstall
import bootCheck
import datetime
import time
import os
import shutil
import sys
from cpu_ram_usage import getVersionInfo
import logging

logging.basicConfig(filename=r"Logs\\Logs.txt",level=logging.DEBUG)

def saveData():
	currentDT = datetime.datetime.now()
	currentTime = currentDT.strftime("%Y%m%d-%H%M%S")
	newpath = os.path.join('c', os.sep, "Users", "Administrator", "Desktop", "perf_rc_suite", "Results", currentTime + " PRC Results " + str(getVersionInfo()))
	if not os.path.exists(newpath):
		os.makedirs(newpath)
	try:
		shutil.move(r'results.json', newpath)
		logging.info(str(datetime.datetime.now()) + " Saving boot result file")
	except Exception as e1:
		print("Error in moving file - " + str(e1))
		logging.warning(str(datetime.datetime.now()) + " Error saving boot result file - " + str(e1))
	try:
		shutil.move(r'Results\SubBootPerf', newpath)
		logging.info(str(datetime.datetime.now()) + " Saving Subsequent boot PerfView result")
	except Exception as e2:
		print("Error in moving file - " + str(e2))
		logging.warning(str(datetime.datetime.now()) + " Error Saving Subsequent boot PerfView result - " + str(e2))
	try:
		shutil.move(r'Results\Benchmarking', newpath)
		logging.info(str(datetime.datetime.now()) + " Saving Benchmarking results")
	except Exception as e3:
		print("Error in moving file - " + str(e3))
		logging.warning(str(datetime.datetime.now()) + " Error saving Benchmarking results - " + str(e3))
	try:
		shutil.move(r'Results\RAM_CPU', newpath)
		logging.info(str(datetime.datetime.now()) + " Saving RAM CPU results")
	except Exception as e4:
		print("Error in moving file - " + str(e4))
		logging.warning(str(datetime.datetime.now()) + " Error Saving RAM CPU results - " + str(e4))
	print("Finished")


def ReleaseCriteria():
	print(os.getcwd())
	with open(r'flags.json') as f:
		data = json.load(f)
	if data["builds"]["1"]["isFinished"] == 1 and data["builds"]["2"]["isFinished"] == 1:
		print("Finished readings for all builds")
		sys.exit(0)
	curBuild = data["builds"]["current"]
	logging.info(str(datetime.datetime.now()) + " Starting test on Build number - " + str(curBuild)) 
	testCases = ["cpuram", "fboot", "sboot", "sboot_p"]
	for test in testCases:
		if data["builds"][str(curBuild)]["toTest"][str(test)] == 0:
			data[str(test)]["CompletionFlag"] = 1
			logging.info(str(datetime.datetime.now()) + " Not testing for current build - " + str(test))
	with open(r'flags.json', 'w') as json_file:
		json.dump(data, json_file)
	
	if data["builds"][str(curBuild)]["toTest"]["fboot"] == 0:
		print("Necessary first boot started")
		logging.info(str(datetime.datetime.now()) + " Starting necessary First Boot")
		print("Before install")
		launchinstall.installBluestacks()
		print("Installed")
		time.sleep(5)
		bootTime = bootCheck.startBootTest(0)
		logging.info(str(datetime.datetime.now()) + " Starting OTS")
		sikuliController.runSikuli(0)
		logging.info(str(datetime.datetime.now()) + " Completed OTS")
		sikuliController.runSikuli(1)
		logging.info(str(datetime.datetime.now()) + " Quit Emulator")
		data["fboot"]["CompletionFlag"] = 1
	
	if data["fboot"]["CompletionFlag"] == 0:
		print("\nStarting First Boot Test\nWaiting for 30 seconds\n")
		logging.info(str(datetime.datetime.now()) + " Starting First Boot Test (RC)")
		time.sleep(30)
		if stable_cpu.main(0,60) == True:
			logging.info(str(datetime.datetime.now()) + " Machine stable, continuing with test")
			boot_result = PRC_Boot.rcBoot(0)
		if data["fboot"]["IterationFlag"] != data["fboot"]["TotalIterations"]:
			print("restarting Machine")
			logging.info(str(datetime.datetime.now()) + " Restarting Machine for First Boot")
			restart_machine.restart()
		else:
			logging.info(str(datetime.datetime.now()) + " Last First boot, starting OTS")
			sikuliController.runSikuli(0)
			logging.info(str(datetime.datetime.now()) + " Quitting Emulator")
			sikuliController.runSikuli(1)
		print(boot_result)
	else:
		print("First Boot Data recorded")
		logging.info(str(datetime.datetime.now()) + " First Boot data Recorded")
	
		
	if data["sboot"]["CompletionFlag"] == 0:
		print("\nStarting Subsequent Boot Test\nWaiting for 15 seconds\n")
		logging.info(str(datetime.datetime.now()) + " Starting Subsequent Boot Test (RC)")
		time.sleep(15)
		boot_result = PRC_Boot.rcBoot(1)
		print(boot_result)
	else:
		print("Subsequent Boot Data recorded")
		logging.info(str(datetime.datetime.now()) + " Subsequent Boot Data Recorded")
	
	if data["sboot_p"]["CompletionFlag"] == 0:
		print("\nStarting Subsequent Boot with PerfView Test\nWaiting for 15 seconds\n")
		logging.info(str(datetime.datetime.now()) + " Starting Subsequent Boot with PerfView Test (RC)")
		time.sleep(15)
		boot_result = PRC_Boot.rcBoot(2)
		print(boot_result)
	else:
		print("Subsequent Boot with PerfView Data recorded")
		logging.info(str(datetime.datetime.now()) + " Subsequent Boot with PerfView data recorded")
	
	if data["cpuram"]["CompletionFlag"] == 0:
		if data["cpuram"]["IterationFlag"] == 1:
			if data["cpuram"]["firstRestart"] == 0:
				print("Updating flag for restart")
				with open(r'flags.json') as f:
					data = json.load(f)
				data["cpuram"]["firstRestart"] = 1
				with open(r'C:\Users\Administrator\Desktop\perf_rc_suite\flags.json', 'w') as json_file:
					json.dump(data, json_file)
				print("restarting Machine")
				logging.info(str(datetime.datetime.now()) + " Restarting Machine for first CPU RAM recording")
				restart_machine.restart()
		
		print("\nStarting CPU/RAM Test\nWaiting for 30 seconds\n")
		logging.info(str(datetime.datetime.now()) + " Starting CPU RAM Test (RC)")
		time.sleep(30)
		PRC_CPU_RAM.RecordcpuramData()
		print("Cpu ram completed")
		if data["cpuram"]["IterationFlag"] != data["cpuram"]["TotalIterations"]:
			print("restarting Machine")
			sikuliController.runSikuli(1)
			time.sleep(15)
			logging.info(str(datetime.datetime.now()) + " Restarting Machine for next CPU RAM test")
			restart_machine.restart()
		else:
			#print("Exiting BS from cpu ram")
			sikuliController.runSikuli(1)
			time.sleep(15)
	else:
		print("CPU and RAM Data recorded")
	#print("reading flag")
	with open(r'flags.json') as f:
		data = json.load(f)
	if data["fboot"]["CompletionFlag"] == 1 and data["sboot"]["CompletionFlag"] == 1 and data["sboot_p"]["CompletionFlag"] == 1 and data["cpuram"]["CompletionFlag"] == 1:
		logging.info(str(datetime.datetime.now()) + " All test cases completed")
		emuDir = os.path.join(os.getcwd(), "Emulator")
		list = os.listdir(emuDir)
		with open(r'flags.json') as f:
			data = json.load(f)
		for i in range(1,len(list)+1):
			#print("checking isFinished")
			flag = data["builds"][str(i)]["isFinished"]
			if flag == 0:
				#print("changing and resetting flags")
				data["builds"][str(i)]["isFinished"] = 1
				data["fboot"]["CompletionFlag"] = 0
				data["sboot"]["CompletionFlag"] = 0
				data["sboot_p"]["CompletionFlag"] = 0
				data["cpuram"]["CompletionFlag"] = 0
				data["cpuram"]["firstRestart"] = 0
				if i == len(list):
					data["builds"]["current"] = 1
				elif i < len(list):
					data["builds"]["current"] += 1
				break
		logging.info(str(datetime.datetime.now()) + " Resetting all flags after Build data recorded")
		#elif data["builds"]["2"]["isFinished"] == 0:
		#	data["builds"]["2"]["isFinished"] = 1
		#	data["fboot"]["CompletionFlag"] = 0
		#	data["sboot"]["CompletionFlag"] = 0
		#	data["sboot_p"]["CompletionFlag"] = 0
		#	data["cpuram"]["CompletionFlag"] = 0
		
		saveData()
		
		BluestacksUninstall.uninstall()
		print("Sleeping for Uninstall")
		time.sleep(20)
		
		with open(r'flags.json', 'w') as json_file:
			json.dump(data, json_file)
		
	if data["builds"]["1"]["isFinished"] == 1 and data["builds"]["2"]["isFinished"] == 1:
		print("Finished readings for all builds")
		sys.exit(0)
	elif data["builds"]["1"]["isFinished"] == 1 and data["builds"]["2"]["isFinished"] == 0:
		print("restarting")
		logging.info(str(datetime.datetime.now()) + " Restarting Machine to start testing next build")
		restart_machine.restart()

ReleaseCriteria()
#saveData()