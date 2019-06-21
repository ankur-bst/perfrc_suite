
import psutil
import time
from statistics import stdev
import csv

max_avg_cpu = 0
max_stdev = 40

# Method to collect CPU usage for specified time
def collect_cpu(count):					
	print("Collecting CPU for", count, "secs... ")
	cpu_usage=[]
	start = time.time()
	for i in range(0,count):
		perc = psutil.cpu_percent(interval=1)
		cpu_usage.append(perc)
	cpu_avg = sum(cpu_usage)/len(cpu_usage)
	cpu_stdev = stdev(cpu_usage)
	return cpu_usage, cpu_avg, cpu_stdev

# Check for CPU stability for dur time
def check_cpu(dur):
	global max_cpu
	flag = False
	
	print("Checking for stable CPU")

	temp_cpu, temp_avg, temp_stdev = collect_cpu(dur)
	
	print(temp_cpu)
	print("Avg. CPU for",dur,"secs:",temp_avg)
#	print("Max CPU: ", max(temp_cpu))
#	print("Std. Dev. :", temp_stdev)
	
	if ((temp_avg <= max_avg_cpu) & (temp_stdev <= max_stdev)):
		print ("Avg. CPU:", temp_avg, " <", max_avg_cpu)
		print ("Std. dev:", temp_stdev, " <", max_stdev)
		print("CPU is stable... ")
		return True
	else:
		print ("Avg. CPU:", temp_avg, " >", max_avg_cpu)
		print ("Std. dev is", temp_stdev, " >", max_stdev)	
		print("CPU is Unstable... ")
		return False	

def main(state, time):		# State is Machine state and time is duration to check for CPU
	global max_avg_cpu	
	
	if (state==0):				# Idle state machine
		max_avg_cpu=5
	elif (state==1):			# Client state machine
		max_avg_cpu=5
	else:
		max_avg_cpu=100
	
	return check_cpu(time)

	'''
	if check_cpu(time):			# To check if CPU is unstable for a very long time
		return True
	else:
		return False
	
	elif counter>=3 :
		print("\nCPU is unstable. \nPlease restart the machine.")
		return False	
	else:
		counter+=1
	'''
	
#main(1, 10)

