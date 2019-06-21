import time
import datetime
import compare
import saveScrCap
import simKeyPress
import launchemulator
import json
import PerfView
from pywinauto.findwindows import find_window
from pywinauto.win32functions import SetForegroundWindow
import logging

logging.basicConfig(filename=r"Logs\Logs.txt",level=logging.DEBUG)

#currentDT = datetime.datetime.now()
#startTime = currentDT.strftime("%H%M%S")
#startTime = time.time()
#ctr = 1
#bCheck = False

#time.sleep(5)
def startBootTest(testcase):
	#curTime = time.time()
	ctr = 1
	failCounter = 0
	failCheck = False
	bCheck = False
	if testcase == 0:
		with open(r'flags.json') as f:
			data = json.load(f)
		curBuild = data["builds"]["current"]
		if data["builds"][str(curBuild)]["defOTS"] == 1:
			origImgPath = r'Boot\images\FirstBoot\originaldef.png'
		elif data["builds"][str(curBuild)]["defOTS"] == 0:
			origImgPath = r'Boot\images\FirstBoot\original.png'
		currentImgPath = r'Boot\images\FirstBoot\current-' + str(ctr) + '.png'
	if testcase == 1:
		origImgPath = r'Boot\images\subsequentBoot\original.png'
		currentImgPath = r'Boot\images\subsequentBoot\current-' + str(ctr) + '.png'
	if testcase == 2:
		origImgPath = r'Boot\images\subsequentBoot_Perfview\original.png'
		currentImgPath = r'Boot\images\subsequentBoot_Perfview\current-' + str(ctr) + '.png'
		with open(r'flags.json') as f:
			data = json.load(f)
		iteration = data["sboot_p"]["IterationFlag"]
	if testcase == 2:
		PerfView.startCollect(iteration, 'SubBootPerf')
	#startTime = time.time()
	#print("diff: " + str(startTime- curTime))
	launchemulator.launch()
	startTime = time.time()
	#time.sleep(12)
	#curTime = time.time()
	#print(curTime - startTime)
	time.sleep(6)
	while not bCheck:
		try:
			#if ctr == 1:
				#time.sleep(3)
				#SetForegroundWindow(find_window(title='BlueStacks'))
				#time.sleep(2)
			#time.sleep(12)	
			simKeyPress.TakeSS()
			stopTime = time.time()
			#print("Elapsed Time: " + str(stopTime - startTime) + " s")
			#print("Checking boot - " + str(ctr))
			saveScrCap.saveCurrent(currentImgPath)
			try:
				res = compare.checkBootImg(origImgPath, currentImgPath)
			except Exception as e:
				print("Couldn't retrieve SSIM value (non def) - " + str(e))
				failCheck = True
				if failCounter == 50:
					print("Boot Test Failed")
					logging.info(str(datetime.datetime.now()) + " Boot Test Failed")
					break
			if testcase == 0 and failCheck:
				try:
					res = compare.checkBootImg(origImgPath, currentImgPath)
				except Exception as e:
					print("Couldn't retrieve SSIM value (def) - " + str(e))
			#print(res)
			#if res["MSE"] <= 800 and res["SSIM"] >= 0.9:
			if res["SSIM"] >= 0.9:
				bCheck = True
				print("Boot Test Passed")
				logging.info(str(datetime.datetime.now()) + " Boot Successful")
			else:
				ctr += 1
		except Exception as e:
			print("Couldn't compare images : error - " + str(e))
			failCounter += 1
			if failCounter == 50:
				print("boot test failed")
				logging.info(str(datetime.datetime.now()) + " Boot Unsuccessful")
				break
		
	if testcase == 2:
		PerfView.stopCollect(iteration, 'SubBootPerf')
		PerfView.killPerfView()	
	bootTime = stopTime - startTime
	print(bootTime)
	print("Client Booted")
	return(bootTime)
			#booted = Utils.is_android_booted()
			#if booted:
			#	print("android Booted")
			#	bCheck = True
			#	if testcase == 2:
			#		PerfView.stopCollect(1)
			#		PerfView.killPerfView()
			#	return(bootTime)
	
		
#print(startBootTest(0))