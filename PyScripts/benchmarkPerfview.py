
#Only works for 1280 x 720 screen resolution and 240 DPI

import subprocess
import os
import time
import PerfView

#height = 1280
#width = 720
height = 1600
width = 900
BS4_PATH = "C:\\Program Files\\BlueStacks\\"
SHELL = "hd-adb shell "

# Connect to ADB
def adb_connect():
	print('\nConnecting to ADB')
	subprocess.call("curl http://127.0.0.1:9999/connecthost")
	time.sleep(10)
	print('ADB connected\n')
	return True
	
# Install app from PlayStore		
def install_app():
	global BS4_PATH
	global SHELL
	
	os.chdir(BS4_PATH)
	subprocess.call(SHELL+r'am start -a android.intent.action.VIEW -d "market://details?id=com.futuremark.dmandroid.application"')	#Open Playstore page
	time.sleep(5)									#Wait for page to open
	#subprocess.call(SHELL+"input tap 1150 309")		#Tap on Install
	subprocess.call(SHELL+"input tap "+ str(0.9*height) + " " + str(0.43*width))
	time.sleep(30)
	print('Benchmark app is installed.')
	return True

#	Setup 3D Benchmark app after install
def benchmark_app_setup():
	global height
	global width
	global BS4_PATH
	
	os.chdir(BS4_PATH)
	subprocess.call(r'hd-adb shell am start -n com.futuremark.dmandroid.application/com.futuremark.flamenco.ui.splash.SplashPageActivity')
	time.sleep(5)
	#subprocess.call("hd-adb shell input tap "+str(0.86*width)+" "+str(0.58*height))	#Accept T&C
	subprocess.call("hd-adb shell input tap "+str(0.88*width)+" "+str(0.56*height))
	time.sleep(2)
	#subprocess.call("hd-adb shell input tap "+str(0.70*width)+" "+str(0.58*height))	#Accept Android permissions
	subprocess.call("hd-adb shell input tap "+str(0.88*width)+" "+str(0.54*height))
	time.sleep(2)
	#subprocess.call("hd-adb shell input tap "+str(0.90*width)+" "+str(0.15*height))	#Skip tutorial
	subprocess.call("hd-adb shell input tap "+str(0.87*width)+" "+str(0.36*height))
	time.sleep(2)
	#subprocess.call(SHELL+"input tap "+str(0.95*width)+" "+str(0.06*height))		#Open Settings dropdown
	#subprocess.call(SHELL+"input tap "+str(0.95*width)+" "+str(0.06*height))		#Open Settings
	subprocess.call(SHELL+"input tap "+str(0.95*width)+" "+str(0.05*height))		#Open Settings dropdown
	subprocess.call(SHELL+"input tap "+str(0.95*width)+" "+str(0.05*height))		#Open Settings
	time.sleep(4)
	
	#subprocess.call(SHELL+"input tap "+str(0.9*width)+" "+str(0.31*height))		#Disable demo
	subprocess.call(SHELL+"input tap "+str(0.92*width)+" "+str(0.25*height))
	time.sleep(1)
	
	#subprocess.call(SHELL+"input tap "+str(0.94*width)+" "+str(0.35*height))		#Open dropdown
	subprocess.call(SHELL+"input tap "+str(0.92*width)+" "+str(0.3*height))
	time.sleep(1)
	#subprocess.call(SHELL+"input tap "+str(0.85*width)+" "+str(0.6*height))		#Install Icestorm
	subprocess.call(SHELL+"input tap "+str(0.92*width)+" "+str(0.5*height))
	#	time.sleep(10)
	
	subprocess.call(SHELL+"input tap "+str(0.06*width)+" "+str(0.06*height))		#Return to home screen
	time.sleep(1)

#check for GLThread that runs during benchmark 					CODE REVIEW       RISK: can skip a step because of 5 second sleep
def checkThread():
	ctr = 0
	time.sleep(5)
	while True:
		x = subprocess.call(BS4_PATH +'hd-adb shell top -t -n 1 | grep GLThread')
		if x == 1:
			print("Couldnt find thread")
			ctr += 1			#increment counter by 1 to denote benchmark tests completed
			if ctr == 3:
				break
			time.sleep(5)
		time.sleep(1)
	return(0)
	
#Run Icestorm Test
def launch_test(iteration):
	global height
	global width
	global BS4_PATH
	
	os.chdir(BS4_PATH)
	subprocess.call(r'hd-adb shell am start -n com.futuremark.dmandroid.application/com.futuremark.flamenco.ui.splash.SplashPageActivity')
	time.sleep(10)
	subprocess.call(SHELL+"input tap "+str(0.60*width)+" "+str(0.12*height))		#Switch to Icestorm tab
	time.sleep(20)
	#subprocess.call(SHELL+"input tap "+str(0.90*width)+" "+str(0.47*height))		#Launch the test
	subprocess.call(SHELL+"input tap "+str(0.92*width)+" "+str(0.64*height))
	PerfView.startCollect(1, 'Benchmarking')
	if checkThread() == 0:
		PerfView.stopCollect(1, 'Benchmarking')
		PerfView.killPerfView()
	#time.sleep(100)
	
#Extract Benchmark file and rename Zip file
def get_data(iter):
	global BS4_PATH
	
	orig_path = os.getcwd()
	os.chdir(BS4_PATH)
	res = subprocess.check_output(SHELL+"cd /sdcard/3DMarkAndroid && ls -t | head -n1")
	res = str(res)
	res = res.split("'")[1].split('\\')[0]
	subprocess.call("hd-adb pull /sdcard/3DMarkAndroid/"+res+" \""+orig_path+"\"/.")
	#subprocess.call(SHELL+" rm -rf /sdcard/3DMarkAndroid/*")			#Delete the file    (is there any purpose - discuss w/  ankur)
	os.chdir(orig_path)
	print(os.getcwd())
	os.rename(res, str(iter)+".3D.Benchmark.zip")
	
def kill_app():
	global BS4_PATH
	os.chdir(BS4_PATH)
	os.system(SHELL + "am force-stop com.futuremark.dmandroid.application")

def main(count):
	for i in (1, count):
		get_data(i)
	
# TRIAL CHECKS
#adb_connect()
#install_app()
#benchmark_app_setup()
#launch_test(1)
#checkThread()
#get_data(1)
#main(1)
