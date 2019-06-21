import os
import re
import sys
import glob
import time
import ntpath
import psutil
import shutil
import string
import logging
#import urllib2
import zipfile
import traceback
import subprocess as subp

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

def is_64_windows():
    return 'PROGRAMFILES(X86)' in os.environ

def get_os_version():
    """
    Get's the OS major and minor versions.  Returns a tuple of
    (OS_MAJOR, OS_MINOR).
    """
    os_version = OSVERSIONINFOEXW()
    os_version.dwOSVersionInfoSize = ctypes.sizeof(os_version)
    retcode = ctypes.windll.Ntdll.RtlGetVersion(ctypes.byref(os_version))
    if retcode != 0:
        raise Exception("Failed to get OS version")

    return os_version.dwMajorVersion, os_version.dwMinorVersion


def get_windows_name():
    majorver, minorver = get_os_version()

    if majorver < 5:
        return("ERROR")
    elif (majorver == 5):
        return("XP")
    elif (majorver == 6) and (minorver == 0):
        return("Vista")
    elif (majorver == 6) and (minorver == 1):
        return("7")
    elif (majorver == 6) and (minorver == 2):
        return("8")
    elif (majorver == 6) and (minorver == 3):
        return("8.1")
    elif (majorver == 10):
        return("10")
    else:
        return("ERROR")


def is_android_booted():
    import urllib.request

    androidpingurl = "http://localhost:9999/ping"
    response = ""
    try:
      res = urllib.request.urlopen(androidpingurl)
      response = res.read()
    except:
      pass

    if not response or (res.code != 200):
        return False
    else:
        print(response)
        return True


def is_process_running(pname):
    try:
        for p in psutil.process_iter():
            try:
                if p.name() == pname:
                    return True
            except psutil.Error:
                pass

        return False

    except Exception as e:
        logging.exception("Error in is_process_running" + str(e))
        return False


def get_last_app():
    try:
        url = "http://127.0.0.1:2871/appdisplayed"

        resp = get_HTTP_data(url)
        pattern1 = r'\[\{"success": true, "LastAppDisplayed":'
        pattern2 = r'\}\]'
        t1 = re.split(pattern1, resp)[1]
        response = re.split(pattern2, t1)[0].strip()
        return response

    except Exception as e:
        logging.exception("Error in get_last_app\n" + str(e))
        logging.exception(traceback.format_exc())
        return None


def match_pattern(string, pattern):
    match_obj = re.search(pattern, string)

    if match_obj is not None:
        return True
    else:
        return False


def get_filename_from_path(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def check_file_exists(path):
    try:
        logging.info("Checking if " + get_filename_from_path(path) + " exists")
        return (os.path.exists(path))
    except Exception as e:
        logging.exception("Error in checking for existence of file")
        return False

def countdown(x):
    for t in range(x, -1, -1):
        sf = "{:02d}:{:02d}".format(*divmod(t, 60))
        sys.stdout.write(sf + "\r")
        time.sleep(1)
    logging.info("")


def launch_process(exepath, args, waitForExit, isShell, timeout=10):

    # Flush all pending output to stdout. POpen might screw that up so added as a precaution
    sys.stdout.flush()

    ret_code = None
    logging.info("waitForExit: " + str(waitForExit))
    logging.info("isShell: " + str(isShell))

    try:
        command = "\"{0}\"".format(exepath)

        if not args :
            logging.info("Launching process: "+ exepath + " timeout: "+ str(timeout))
            pass
        else:
            logging.info("Launching process: "+ exepath + " with args: " + str(args) + " timeout: "+ str(timeout))
            command += " " + args

        proc_info = subp.Popen(command, shell=isShell)

        logging.info("process id of launched process is process:"+ str(proc_info.pid))

        #XXX: Is this hacky?, how to get exitcode if proc was not exitied?
        if not waitForExit:
            return

        killed = False
        i=0
        time_count = timeout/5

        while proc_info.poll() is None:
            i += 1

            if (i>5):
                proc_info.kill()
                killed = True
                logging.info( "process killed.." )
                break

            time.sleep(time_count)

        if not killed:
            ret_code = proc_info.returncode

    except:
        logging.exception("launch_process error")

    logging.info("Process return code: " + str(ret_code))

    return ret_code

def launch_process_out(exepath, args, timeout=10):
    sys.stdout.flush()

    command = "\"{0}\"".format(exepath)

    if args:
        command = exepath + " " + args

    proc_info = subp.Popen(command, stdout=subp.PIPE)
    (output, err) = proc_info.communicate()

    killed = False
    i=0
    time_count = timeout/5

    while proc_info.poll() is None:
        i += 1

        if (i>5):
            proc_info.kill()
            killed = True
            logging.info( "process killed.." )
            break

        time.sleep(time_count)

    logging.debug(output)
    return output

def compare_lists(list1,list2):
    logging.info("Comparing lists")
    ret = True

    l1= len(list1)
    l2= len(list2)
    if ((l1 ==0) or (l2 == 0)):
        logging.info("Empty/Null lists:-" )
        logging.info(list1)
        logging.info(list2)
    else:
        if (l1 != l2):
        #compare lenghts if lens diff. return False
            logging.info("list1: " )
            logging.info(lPmlist )
            logging.info( "list2 : "   )
            logging.info( lAppInstallated  )
        else:
            logging.info("list1: " )
            logging.info(lPmlist )
            logging.info( "list2 : "   )
            logging.info( lAppInstallated  )
            lPmlist.sort()
            lAppInstallated.sort()
            #print "\n####reachedhere\n"
            if ( cmp(lPmlist, lAppInstallated) ==0 ):
                #print "\n####eachedhere\n"
                op=True
    return op

def append_to_file(fPath, line):
    with open(fPath, "a") as f:
        f.write(line + "\n")

def get_file_contents(fPath):
    with open(fPath, "r") as f:
        return f.read()

def create_dir(dirPath):
    if not os.path.exists(dirPath):
        print("Creating dir : " + dirPath)
        os.makedirs(dirPath)

def delete_file(fPath):
    try:
        os.remove(fPath)
        logging.info(fPath + " deleted")
    except OSError:
        pass

def delete_dir(dirPath):
    logging.info("Deleting dir: " + str(dirPath))
    shutil.rmtree(dirPath)
    logging.info("Deleted")

def copy_file(src, dst):
    dst_dir = os.path.dirname(dst)
    if not os.path.exists(dst_dir):
        logging.info("Destination dir does not exist, creating: " + dst_dir)
        os.makedirs(dst_dir)
    logging.info("Copying file from {0} to {1}".format(str(src), str(dst)))

    shutil.copyfile(src, dst)
    logging.info("Copied sucessfully")

def move_file(src, dst):
    dst_dir = os.path.dirname(dst)
    if not os.path.exists(dst_dir):
        logging.info("Destination dir does not exist, creating: " + dst_dir)
        os.makedirs(dst_dir)
    logging.info("Moving file from {0} to {1}".format(str(src), str(dst)))

    shutil.move(src, dst)
    logging.info("Moved sucessfully")

def copy_dir(src, dst):
    logging.info("copying dir from {0} to {1}".format(src, dst))
    shutil.copytree(dirPath)
    logging.info("copied")

def replace_substr(origStr, subStr, newSubStr, numOccurence=1):
    return string.replace(origStr, subStr, newSubStr, numOccurence)

def get_system_var(varName):
    return os.getenv(varName, "").strip()

def get_matching_files(pattern):
    return glob.glob(pattern)

def is_valid_email(email):
    if not EMAIL_REGEX.match(email):
        return False
    else:
        return True

'''
def basic_file_downloader(url, dest):
    filedata = urllib2.urlopen(url)
    datatowrite = filedata.read()

    with open(dest, 'wb') as f:  
        f.write(datatowrite)
'''

def extract_zip(src, dst):
    zip_ref = zipfile.ZipFile(src, 'r')
    zip_ref.extractall(dst)
    zip_ref.close()
