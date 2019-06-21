import psutil
import statistics
import os
import datetime
import csv
import winreg
import logging

logging.basicConfig(filename=r"Logs\Logs.txt",level=logging.DEBUG)
memory=[]
cpu=[]
time_recorded=[]

def getVersionInfo():
# Open the key and return the handle object.
	try:
		hKey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "Software\\BlueStacks", 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
		result = winreg.QueryValueEx(hKey, "Version")
		#logging.info(str(datetime.datetime.now()) + ' Found client version for BS4')
		emulatorName="Bluestacks 4 version:- "
		logging.info(str(datetime.datetime.now()) + " Getting Bluestacks Version Information")
	except Exception as e:
		print("Couldn't find registry.. Error - " + str(e))
		logging.info(str(datetime.datetime.now()) + " Couldn't find registry.. Error - " + str(e))

	winreg.CloseKey(hKey)
    # Return only the value from the resulting tuple (value, type_as_int).
	return str(result[0])

def avg(list):
	total=0
	try:
		for l in list:
			total+=l
	except Exception as e:
		print("Type Error: Value not readable for average")
		return None
	result=total/(len(list))
	return round(result, 2)

#t=int(input("Please enter time in seconds to take readings in idle state: "))

def recordCpuRam(t, stage, iteration):
	logging.info(str(datetime.datetime.now()) + " Started recording cpu/ram data for iteration " + str(iteration) + " and stage " + str(stage))
	for i in range(t):
		print(i+1)
		mem = psutil.virtual_memory()
		cpu.append(psutil.cpu_percent(interval=1))
		memory.append(round(mem.used/1048576,2))
		time_recorded.append(str(datetime.datetime.now()))

	cpudetails = "Average of CPU used: " + str(avg(cpu)) + " (s " + str(round(statistics.stdev(cpu),2)) + ", r " + str(min(cpu)) + "-" + str(max(cpu)) + "%)"

	ramdetails = "Average of Used Memory: " + str(avg(memory)) + " (s " + str(round(statistics.stdev(memory),2)) + ", r " + str(min(memory)) + "-" + str(max(memory)) + " MB)"

	print(cpudetails)
	print(ramdetails)

	ResultFile = str(time_recorded[0]) + "PRC_ramcpu.csv"

	#dir ="C:\Users\Administrator\Desktop\Perf RC Automation\Results\RAM_CPU"

	Version = getVersionInfo()
	currentDT = datetime.datetime.now()
	currentTime = currentDT.strftime("%H%M%S")

	newpath = os.path.join('c', os.sep, "Users", "Administrator", "Desktop", "perf_rc_suite", "Results", "RAM_CPU", Version, "Iteration - " + str(iteration), "Stage - " + str(stage))
	if not os.path.exists(newpath):
		os.makedirs(newpath)
		logging.info(str(datetime.datetime.now()) + " Creating Result directory for RAM CPU readings; stage- " + str(stage) + ", iteration- " + str(iteration))
	with open(os.path.join('c', os.sep, "Users", "Administrator", "Desktop", "perf_rc_suite", "Results", "RAM_CPU", Version, "Iteration - " + str(iteration), "Stage - " + str(stage), currentTime + " PRC_ramcpu.csv"), 'w', newline='') as f:
		newFileWriter=csv.writer(f)
		logging.info(str(datetime.datetime.now()) + " Writing cpu/ram data to csv file")
		newFileWriter.writerow(["TimeStamp", "CPU %", "RAM (MB)"])
		for i in range(0,len(cpu)):
			newFileWriter.writerow([time_recorded[i], cpu[i], memory[i]])
		newFileWriter.writerow([cpudetails])
		newFileWriter.writerow([ramdetails])