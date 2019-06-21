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

def file_input(text_input):
    try:
        my_dir = "C:\\Users\\Administrator\\Desktop\\Perf RC Automation\\Logs\\"
        my_file=file(my_dir + "Logs.txt", "a")
        my_file.write(text_input)
        my_file.close
    except:
        print "Issue writing in File..."

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
   