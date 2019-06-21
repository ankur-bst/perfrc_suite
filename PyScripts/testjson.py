import time
import os
import subprocess as subp
import sys
import logging
import datetime
import json

with open(r'C:\Users\Administrator\Desktop\Perf RC Automation\flags.json') as f:
	data = json.load(f)
print(data)
print(data.keys())
print(data.values())
print(data["IterationFlag"])

data["IterationFlag"] += 1

x = data["IterationFlag"]

print(x)

print(data)

with open(r'C:\Users\Administrator\Desktop\Perf RC Automation\flags.json', 'w') as json_file:
	json.dump(data, json_file)