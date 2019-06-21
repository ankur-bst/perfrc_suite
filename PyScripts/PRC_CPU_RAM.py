import os
import sys
import logging
import time
import datetime
import subprocess as subp
import launchemulator as startBS
import cpu_ram_usage as CRU
import launch_android_settings as androidSetting
import json
import stable_cpu
import logging

logging.basicConfig(filename=r".\..\Logs\Logs.txt",level=logging.DEBUG)

with open(r'C:\Users\Administrator\Desktop\perf_rc_suite\flags.json') as f:
	data = json.load(f)

def RecordcpuramData():
	stageFlag = 1
	iterFlag = data["cpuram"]["IterationFlag"]
	Iterations = data["cpuram"]["TotalIterations"]
	t = data["cpuram"]["time_to_record"]
	isCompleted = data["cpuram"]["CompletionFlag"]
	try:
		print("here1")
		if isCompleted == 1:
			return
		if isCompleted == 0:
			print("here2")
			if iterFlag <= Iterations:
				print("here3")
				if stageFlag == 1:
					print("here4")
					if stable_cpu.main(0,60) == True:
						logging.info(str(datetime.datetime.now()) + " Recording CPU RAM data for Idle Machine")
						CRU.recordCpuRam(t, stageFlag, iterFlag)
					stageFlag += 1
				if stageFlag == 2:
					startBS.launch()
					print("sleeping")
					time.sleep(100) #Increase sleep time if cpu unstablity presists
					print("waking up")
					if stable_cpu.main(0,60) == True:
						logging.info(str(datetime.datetime.now()) + " Recording CPU RAM data when Client Running")
						CRU.recordCpuRam(t, stageFlag, iterFlag)
					stageFlag += 1
				if stageFlag == 3:
					androidSetting.launchSettings()
					time.sleep(10)
					if stable_cpu.main(0,60) == True:
						logging.info(str(datetime.datetime.now()) + " Recording CPU RAM data on Settings app")
						CRU.recordCpuRam(t, stageFlag, iterFlag)
					if data["cpuram"]["IterationFlag"] < data["cpuram"]["TotalIterations"]:
						data["cpuram"]["IterationFlag"] += 1
						with open(r'C:\Users\Administrator\Desktop\perf_rc_suite\flags.json', 'w') as json_file:
							json.dump(data, json_file)
					elif data["cpuram"]["IterationFlag"] == data["cpuram"]["TotalIterations"]:
						data["cpuram"]["IterationFlag"] = 1
						data["cpuram"]["CompletionFlag"] = 1
						print("Changing iteration and completion")
						with open(r'C:\Users\Administrator\Desktop\perf_rc_suite\flags.json', 'w') as json_file:
							json.dump(data, json_file)
						logging.info(str(datetime.datetime.now()) + " Changing Completion and resetting Iteration Flag for CPU RAM (After Completion)")
				#sys.exit(0)
	except Exception as e:
		print("CompletionFlag value corrupted; Error - " + str(e))
		logging.warning(str(datetime.datetime.now()) + " Couldn't collect data for current iteration - " + str(e))

#RecordcpuramData()
#print("completed")