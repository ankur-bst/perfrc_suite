import subprocess as subp
import sys
import logging
import datetime
import winreg
import time

logging.basicConfig(filename=r"C:\Users\Administrator\Desktop\perf_rc_suite\Logs\Logs.txt",level=logging.DEBUG)
def uninstall():
	try:
		subp.call(r'C:\Program Files\BlueStacks\HD-Quit.exe')
		print("Quitting Bluestacks")
		time.sleep(15)
		subp.Popen(r'C:\Program Files\BlueStacks\BlueStacksUninstaller.exe -s')
		print("Uninstalling Bluestacks")
		logging.info(str(datetime.datetime.now()) + ' Uninstalling BlueStacks')
	except Exception as e:
		print("Failed to Uninstall. Exiting...")
		logging.warning(str(datetime.datetime.now()) + ' Unable to uninstall Bluestacks; Error - ' + e)
		sys.exit(0)
#uninstall()