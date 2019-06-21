import time
import os
import subprocess as subp
import sys
import logging
import datetime
import winreg


logging.basicConfig(filename=r"C:\Users\Administrator\Desktop\perf_rc_suite\Logs\Logs.txt",level=logging.DEBUG)

adb_path_BS4 = 'C:\\Program Files\\BlueStacks\\HD-Adb.exe'
command_BS4 = adb_path_BS4 + ' shell ps | grep -i settings'

def getApiToken():
# Open the key and return the handle object.
	try:
		hKey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "Software\\BlueStacks", 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
		result = winreg.QueryValueEx(hKey, "ApiToken")
		print(result)
		#logging.info(str(datetime.datetime.now()) + ' Found client version for BS4')
		logging.info(str(datetime.datetime.now()) + " Getting Bluestacks Version Information")
	except Exception as e:
		print("Couldn't find registry.. Error - " + str(e))
		logging.info(str(datetime.datetime.now()) + " Couldn't find registry.. Error - " + str(e))

	winreg.CloseKey(hKey)
    # Return only the value from the resulting tuple (value, type_as_int).
	return str(result[0])

def launchSettings():
	apiToken = getApiToken()
	subp.Popen(r'curl -H "X_api_token:' + apiToken + '" http://127.0.0.1:9999/connecthost')
	subp.Popen(r'c:\program files\bluestacks\hd-adb.exe shell am start -n  com.bluestacks.settings/com.bluestacks.settings.SettingsActivity')
	logging.info(str(datetime.datetime.now()) + ' Launching bluestacks settings- BS4')	
	time.sleep(5)
	subp.Popen(r'c:\program files\bluestacks\hd-adb.exe shell am start -n  com.android.settings/.Settings')
	logging.info(str(datetime.datetime.now()) + ' Launching android settings- BS4')	
	time.sleep(5)
	subp.Popen(r'c:\program files\bluestacks\hd-adb.exe shell system/xbin/bstk/su -c "kill -9 `pidof com.bluestacks.settings`"')
	logging.info(str(datetime.datetime.now()) + ' Killing bluestacks settings process- BS4')
	time.sleep(5)
	if os.path.isfile (adb_path_BS4):
		logging.info(str(datetime.datetime.now()) + ' Following is BS4 settings process running *Before taking readings*')
		with open(r"C:\Users\Administrator\Desktop\perf_rc_suite\Logs\Logs.txt","ab") as output_file:
			subp.Popen(command_BS4,stdout=output_file)