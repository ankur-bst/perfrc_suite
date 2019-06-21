import os
import sys
import logging
import time
import datetime
import subprocess as subp
import launchemulator as startBS
import bootCheck
import json
import BluestacksUninstall
import launchinstall
import sikuliController
import restart_machine
import stable_cpu
import logging

logging.basicConfig(filename=r"Logs\Logs.txt",level=logging.DEBUG)



def FirstBoot():
	with open(r'flags.json') as f1:
		data = json.load(f1)
	resultFilePath = r'results.json'
	if not os.path.isfile(resultFilePath):
		dataDump = {}
		with open(resultFilePath, 'w') as json_file:
			json.dump(dataDump,json_file)
		logging.info(str(datetime.datetime.now()) + " Created new results.json file")
	with open(resultFilePath) as f2:
		result = json.load(f2)
	logging.info(str(datetime.datetime.now()) + " Loaded previous boot results in dict")
	iterFlag = data["fboot"]["IterationFlag"]
	Iterations = data["fboot"]["TotalIterations"]
	isCompleted = data["fboot"]["CompletionFlag"]
	if iterFlag <= Iterations:
		try:
			#print("here1")
			#if isCompleted == 1:
			#	return
			if isCompleted == 0:
				#print("here2")
				#print("Before install")
				launchinstall.installBluestacks()
				print("Installed")
				time.sleep(5)
				if stable_cpu.main(0,60) == True:
					logging.info(str(datetime.datetime.now()) + " Checking for fboot bootup...")
					bootTime = bootCheck.startBootTest(0)
				#sikuliController.runSikuli(1)
				if iterFlag != Iterations:
					BluestacksUninstall.uninstall()
					print("Sleeping for Uninstall")
					time.sleep(20)
				if data["fboot"]["IterationFlag"] < data["fboot"]["TotalIterations"]:
					print("Changing Flag")
					data["fboot"]["IterationFlag"] += 1
					logging.info(str(datetime.datetime.now()) + " Incrementing fboot flag")
					with open(r'C:\Users\Administrator\Desktop\perf_rc_suite\flags.json', 'w') as json_file:
						json.dump(data, json_file)
				elif data["fboot"]["IterationFlag"] == data["fboot"]["TotalIterations"]:
					print("Resetting iterFlag and switching CompletionFlag to 1")
					data["fboot"]["IterationFlag"] = 1
					data["fboot"]["CompletionFlag"] = 1
					with open(r'C:\Users\Administrator\Desktop\perf_rc_suite\flags.json', 'w') as json_file:
						json.dump(data, json_file)
					logging.info(str(datetime.datetime.now()) + " Changing Completion and resetting iteration flag for fboot")
				if iterFlag == 1:
					result.update({"fboot":{}})
				result["fboot"].update({iterFlag: bootTime})
				logging.info(str(datetime.datetime.now()) + " Updating fboot result of iteration - " + str(iterFlag))
				with open(r'C:\Users\Administrator\Desktop\perf_rc_suite\results.json', 'w') as json_file:
						json.dump(result, json_file)
			else:
				print("All iterations completed")
				return(0)
			return(result)
		except Exception as e:
			print("CompletionFlag value corrupted; Error - " + str(e))
			logging.info(str(datetime.datetime.now()) + " Error getting fboot result - " + str(e))

def SubBoot(perfCheck):
	with open(r'C:\Users\Administrator\Desktop\perf_rc_suite\flags.json') as f1:
		data = json.load(f1)
	resultFilePath = r'results.json'
	if not os.path.isfile(resultFilePath):
		dataDump = {}
		with open(resultFilePath, 'w') as json_file:
			json.dump(dataDump,json_file)
		logging.info(str(datetime.datetime.now()) + " Created new results.json file")
	with open(r'C:\Users\Administrator\Desktop\perf_rc_suite\results.json') as f2:
		result = json.load(f2)
	logging.info(str(datetime.datetime.now()) + " Loaded previous results.json file")
	if not perfCheck:
		dictKey = "sboot"
	else:
		dictKey = "sboot_p"
	iterFlag = data[dictKey]["IterationFlag"]
	Iterations = data[dictKey]["TotalIterations"]
	isCompleted = data[dictKey]["CompletionFlag"]
	if iterFlag <= Iterations:
		try:
			#print("here1")
			#if isCompleted == 1:
			#	return
			if isCompleted == 0:
				#print("here2")
				if stable_cpu.main(1,30) == True:
					logging.info(str(datetime.datetime.now()) + " Checking for boot...")
					if not perfCheck:
						bootTime = bootCheck.startBootTest(1)
						#print("test false")
					else:
						bootTime = bootCheck.startBootTest(2)
						#print("test true")
					sikuliController.runSikuli(1)
					#bootTime = 42
					if data[dictKey]["IterationFlag"] < data[dictKey]["TotalIterations"]:
						data[dictKey]["IterationFlag"] += 1
						logging.info(str(datetime.datetime.now()) + " Incrementing " + str(dictKey) + " iteration flag")
						with open(r'C:\Users\Administrator\Desktop\perf_rc_suite\flags.json', 'w') as json_file:
							json.dump(data, json_file)
					elif data[dictKey]["IterationFlag"] == data[dictKey]["TotalIterations"]:
						data[dictKey]["IterationFlag"] = 1
						data[dictKey]["CompletionFlag"] = 1
						with open(r'C:\Users\Administrator\Desktop\perf_rc_suite\flags.json', 'w') as json_file:
							json.dump(data, json_file)
						logging.info(str(datetime.datetime.now()) + " Changing Completion and resetting iteration flag for " + str(dictKey))
					if iterFlag == 1:
						result.update({dictKey:{}})
					result[dictKey].update({iterFlag: bootTime})
					with open(r'C:\Users\Administrator\Desktop\perf_rc_suite\results.json', 'w') as json_file:
						json.dump(result, json_file)
					logging.info(str(datetime.datetime.now()) + " Updating " + str(dictKey) + " result of iteration " + str(iterFlag))
					print("Sleeping for 15 seconds")
					time.sleep(15)
			else:
				print("All iterations completed")
				return(0)
			return(result)
		except Exception as e:
			print("CompletionFlag value corrupted; Error - " + str(e))
			logging.info(str(datetime.datetime.now()) + " Error getting " + str(dictKey) + " result - " + str(e))

def rcBoot(case):
	if case == 0:
		bt = FirstBoot()
	else:
		while True:
			if case == 1:
				bt = SubBoot(False)
			elif case == 2:
				bt = SubBoot(True)
			print(bt)
			if bt == 0:
				break
			time.sleep(15)
	return(bt)
#print(rcBoot(2))