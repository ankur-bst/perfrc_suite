from compareImages import saveScrCap
import simKeyPress
import time

time.sleep(5)
name = 'yolo.png'
simKeyPress.TakeSS()
saveScrCap.saveCurrent(r'C:\Users\Administrator\Desktop\Perf RC Automation\Boot\compareImages\images\\' + name)