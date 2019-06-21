import os
import sys
import logging
import datetime

logging.basicConfig(filename=r"C:\Users\Administrator\Desktop\perf_rc_suite\Logs\Logs.txt",level=logging.DEBUG)

def launch():
	try:
		print("Launching Emulator...")
		logging.info(str(datetime.datetime.now()) + " Starting BlueStacks")
		os.startfile(r'C:\Users\Public\Desktop\BlueStacks.lnk')
	except Exception as e:
		print(e)
		print("Exiting...")
		logging.warning(str(datetime.datetime.now()) + " Could not launch emulator. Error - " + str(e))
		sys.exit(0)
#launch()