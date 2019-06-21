import benchmarkPerfview as bmark
import json
import launchemulator
import time
import bootCheck
import sikuliController

def BenchMarkPerf():
	with open(r'C:\Users\Administrator\Desktop\perf_rc_suite\flags.json') as f1:
		data = json.load(f1)
	if data["bmark_p"]["IterationFlag"] <= data["bmark_p"]["TotalIterations"]:
		if data["bmark_p"]["isCompleted"] == 0:
			boot = bootCheck.startBootTest(1)
			if boot:
				if data["bmark_p"]["IterationFlag"] == 1 and data["bmark_p"]["isAppInstalled"] == 0:
					bmark.adb_connect()
					bmark.install_app()
					bmark.benchmark_app_setup()
					print("Waiting for icestorm installation")
					time.sleep(120)
					sikuliController.runSikuli(1)
					data["bmark_p"]["isAppInstalled"] == 1
					with open(r'C:\Users\Administrator\Desktop\perf_rc_suite\flags.json', 'w') as json_file:
						json.dump(data, json_file)
					return(0)
				bmark.launch_test(data["bmark_p"]["IterationFlag"])
				sikuliController.runSikuli(1)
				data["bmark_p"]["IterationFlag"] += 1
				with open(r'C:\Users\Administrator\Desktop\perf_rc_suite\flags.json', 'w') as json_file:
						json.dump(data, json_file)
				return(1)
				#bmark.get_data(data["bmark_p"]["IterationFlag"])


print(BenchMarkPerf())