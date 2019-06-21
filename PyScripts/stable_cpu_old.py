
import psutil
import time

max_cpu = 0
counter = 0

# Method to collect CPU usage for specified time
def collect_cpu(count):					
	print("Collecting CPU for", count, "secs... ")
	cpu_usage=[]
	start = time.time()
	for i in range(0,count):
		perc = psutil.cpu_percent(interval=1)
		cpu_usage.append(perc)
	cpu_avg = sum(cpu_usage)/len(cpu_usage)
	return cpu_usage, cpu_avg

# Check for CPU stability for dur time
def check_cpu(dur):
	
	global max_cpu
	flag = False
	
	print("Checking for stable CPU")
	while flag != True:	
		temp_dur=dur
		init_cpu, init_avg = collect_cpu(temp_dur)
		print(init_cpu)
		print("Avg. CPU for",temp_dur,"secs:",init_avg)
		print("Max ", max(init_cpu))
		
		if (init_avg >= max_cpu):
			print(init_avg, ">", max_cpu)
			print("CPU UnStable \n Returning back ....")
			continue
		else:
			flag=True 

		temp_dur = int(dur/2)
		print("\n")
		cpu_60sec=[]
		cpu_60sec = init_cpu[-temp_dur:]
		avg_60sec = sum(cpu_60sec)/len(cpu_60sec)
		print("CPU for last",temp_dur,"secs:", cpu_60sec)
		print("Avg. CPU for last", temp_dur,"secs:", avg_60sec)
				
		if (avg_60sec >= max_cpu):
			flag=False
			print(avg_60sec,">", max_cpu)
			print("CPU UnStable \n Returning back ....")
			continue
		
		print("\n")
		temp_dur=int(dur/10)
		for i in range(0,3):
			print ("Collecting temp cpu")
			cpu_temp, avg_temp = collect_cpu(temp_dur)
			print("CPU for",temp_dur,"secs:",cpu_temp)
			print("Avg. CPU for",temp_dur,"secs:",avg_temp, "\n")
			if((avg_temp >= max_cpu) or (max(cpu_temp)>=7)):
				flag = False
				print("CPU UnStable... Need to start again")
				break
	if flag:
		print("Finally CPU is Stable.")
		return True
	else:
		print("CPU is very unstable.")
		return False
	

def main(state, time):		# State is Machine state and time is duration to check for CPU
	global max_cpu			
	global counter
	
	if (state==0):				# Idle state machine
		max_cpu=5
	elif (state==1):			# Client state machine
		max_cpu=7
	else:
		max_cpu=100
	
	if check_cpu(time):			# To check if CPU is unstable for a very long time
		return True
	"""
	elif counter>=3 :
		print("\nCPU is unstable. \nPlease restart the machine.")
		return False
	else:
		counter+=1
	"""
	
#main(0, 120)
