import launchinstall
import bootCheck
import sikuliController
import BluestacksUninstall
import time
import sys

def firstRun():
	print("Before install")
	launchinstall.installBluestacks()
	print("Installed")
	time.sleep(5)
	print("\n\nChecking First Boot\n\n")
	bt = bootCheck.startBootTest(0)
	if bt:
		#print("here")
		print("Time taken to boot = " + str(bt) + " s")
	else:
		print("Failed to boot,  exiting..")
		sys.exit(0)
	time.sleep(10)
	print("\n\nStarting OTS\n\n")
	sikuliController.runSikuli(0)
	time.sleep(10)
	print("\n\nQuitting Bluestacks\n\n")
	sikuliController.runSikuli(1)
	time.sleep(15)
	print("\n\nChecking Subsequent Boot\n\n")
	bt2 = bootCheck.startBootTest(1)
	if bt2:
		#print("here")
		print("Time taken to boot = " + str(bt2) + " s")
	else:
		print("Failed to boot,  exiting..")
		sys.exit(0)
	time.sleep(10)
	print("\n\nQuitting Bluestacks\n\n")
	sikuliController.runSikuli(1)
	time.sleep(15)
	BluestacksUninstall.uninstall()

firstRun()