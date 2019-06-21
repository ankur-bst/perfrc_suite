import timeit
import logging
import datetime,time
import traceback
import platform
import os,sys,re
import glob
import subprocess as subp
import time, json
import os.path
import zipfile
import urllib,urllib2
import argparse
import json
import copy, shutil
import ssl, socket
import xml.etree.ElementTree as ET
from xml.dom import minidom

a = 0
b = 0

def restart():
    try:
        vcCMD = "C:\\Program Files\\BlueStacks\\"
        run(vcCMD + "HD-Quit.exe")
        print "AppPlayer Quit Successfully..."
        wait(15)
        subp.Popen("C:\\ProgramData\\BlueStacks\\Client\\Bluestacks.exe")
        print "AppPlayer started..."
        wait(60)
    except Exception, e:
        print "Issue in Restart function - " + str(e)




def Android_BootupCheck():
    frontend_up()


def frontend_up():
    try:
        start_time = time.time()
        file_input("Start Time : - " + str(start_time) + "\n")
        timeout = 300
        while time.time() - start_time < timeout:
            resp = getLastApp()
            file_input("getLastApp Responce " + str(resp) + "\n")
            if ((resp != None)) :
                file_input("Home app has launched\n")
                print "Android Bootup Check Pass"
                end_time = time.time()
                diff = end_time - start_time
                diff = "%.2f" % diff
                file_input("End Time : - " + str(end_time) + "\n")
                file_input("Android Bootup Time : " + str(end_time) + " - " + str(start_time) + " = " + str(end_time - start_time) + "\n")
                file_input("Sanity Testcase:: Android Bootup Check Successful : PASS\n")
                file_input("Sanity Testcase:: Android First Bootup Time Duration : " + str(diff) + "s\n")
                return 0
            else:
                time.sleep(2)

            if time.time() - start_time > timeout:
                file_input("Something went wrong , Android Up\n")
                file_input("Sanity Testcase:: Android Bootup Check Successful : FAIL\n")
                print "EXIT"
                sys.exit(1001)

    except Exception, e:
        file_input("Error in frontend_up - " + str(e))
        file_input("Sanity Testcase:: Android Bootup Check Successful : FAIL\n")
   


def file_input(text_input):
    try:
        my_dir = "c:\\Sanity_BGP_N_master\\"
        my_file=file(my_dir + "bcgp_log.txt", "a")
        my_file.write(text_input)
        my_file.close
    except:
        print "Issue writing in File..."
        
    
def Install():
    try:
        if exists("1551421542092.png",30):
            click("1551421597524.png")
            
            a = 1

        if a == 0:
            if exists("1522133198332.png",30):
                click("1522133198332.png")
            if exists("1525163571768-2.png",30):
                click("1525163571768-3.png")
            
        if exists("1525163791271.png",200):
            click("1525163791271.png")
            b = 1
            #file_input("Sanity Testcase:: BGP Client Installation Successful : Pass \n")
        if b == 0:
            if exists("1522133198332.png",30):
                click("1522133198332.png")
            if exists("1525163791271.png",200):
                click("1525163791271.png")
             #   file_input("Sanity Testcase:: BGP Client Installation Successful : Pass \n")

        

    except:
        #file_input("Install Fail \n")       
        print "Fail except"




#ApkInstall_UI()
#sys.exit(1001)

#vcCMD = "C:\\Users\\Alok-qa-perf\\Desktop\\MemoryLongRun\\Emulator\\BlueStacks-Installer_4.1.21.2018.exe"
#run(vcCMD)

#subp.Popen(r'C:\Users\Alok-qa-perf\Desktop\MemoryLongRun\Emulator\BlueStacks-Installer_4.1.21.2018.exe')

try:
    Install()
except Exception, e:
    print "Fail"
   # file_input("Issue in Install() - " + str(e))