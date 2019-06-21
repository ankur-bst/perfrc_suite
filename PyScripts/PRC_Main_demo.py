import PRC_Boot
import restart_machine
import stable_cpu
import time
import json

def ReleaseCriteria():
	with open(r'C:\Users\Administrator\Desktop\perf_rc_suite\flags.json') as f:
		data = json.load(f)
	if data["fboot"]["CompletionFlag"] == 0:
		print("\nStarting First Boot Test\nWaiting for 30 seconds\n")
		time.sleep(30)
		if stable_cpu.main(0,60) == True:
			boot_result = PRC_Boot.rcBoot(0)
		if data["fboot"]["IterationFlag"] != data["fboot"]["TotalIterations"]:
			print("restarting Machine")
			restart_machine.restart()
		print(boot_result)
	else:
		print("First Boot Data recorded")

ReleaseCriteria()