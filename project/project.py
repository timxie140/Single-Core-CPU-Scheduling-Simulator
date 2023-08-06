import sys
import math
from numpy import float32 as f32
from drand48 import Rand48
from process import Process
from copy import deepcopy
from FCFS import FCFS
from SJF import SJF
from SRT import SRT
from RR import RR

result_template = {"cpu_utilization" : 0,
          "avg_cpu_burst_time" : 0, "cpubound_avg_cpu_burst_time" : 0, "iobound_avg_cpu_burst_time" : 0,
          "avg_wait_time" : 0, "cpubound_avg_wait_time" : 0, "iobound_avg_wait_time" : 0,
          "avg_turnaround_time" : 0, "cpubound_avg_turnaround_time" : 0, "iobound_avg_turnaround_time" : 0,
          "context_switch" : 0, "cpu_context_switch" : 0, "io_context_switch" : 0,
          "preemption" : 0, "cpu_preemption" : 0, "io_preemption" : 0}

#calculate non-preemptive algo's result
def non_preemptive_result(data, result, t_cs):
    if data["time"] == 0:
        result["cpu_utilization"] = 0
    else:
         result["cpu_utilization"] = math.ceil(((data["total_cpu_elapsed_time"] / data["time"]) * 100) * 1000) / 1000

    if data["total_cpu_burst_times"] == 0:
        result["avg_cpu_burst_time"] = 0
        result["avg_turnaround_time"] = 0
        result["avg_wait_time"] = 0
    else:
        result["avg_cpu_burst_time"] = math.ceil((data["total_cpu_elapsed_time"] / data["total_cpu_burst_times"]) * 1000) / 1000
        result["avg_turnaround_time"] = math.ceil((data["total_turnaround_time"] / data["total_cpu_burst_times"]) * 1000) / 1000
        result["avg_wait_time"] = math.ceil(((data["total_turnaround_time"] / data["total_cpu_burst_times"]) - (data["total_cpu_elapsed_time"]
                                                                                 / data["total_cpu_burst_times"]) - t_cs) * 1000) / 1000

    if data["cpubound_burst_times"] == 0:
        result["cpubound_avg_cpu_burst_time"] = 0
        result["cpubound_avg_wait_time"] = 0
        result["cpubound_avg_turnaround_time"] = 0
    else:
        result["cpubound_avg_cpu_burst_time"] = math.ceil((data["cpubound_cpu_burst_time"] / data["cpubound_burst_times"]) * 1000) / 1000
        result["cpubound_avg_wait_time"] = math.ceil(((data["cpubound_turnaround_time"] / data["cpubound_burst_times"]) - 
                                                  (data["cpubound_cpu_burst_time"] / data["cpubound_burst_times"]) - t_cs) * 1000) / 1000
        result["cpubound_avg_turnaround_time"] = math.ceil((data["cpubound_turnaround_time"] / data["cpubound_burst_times"]) * 1000) / 1000

    if data["iobound_burst_times"] == 0:
        result["iobound_avg_cpu_burst_time"] = 0
        result["iobound_avg_wait_time"] = 0
        result["iobound_avg_turnaround_time"] = 0
    else:
        result["iobound_avg_cpu_burst_time"] = math.ceil((data["iobound_cpu_burst_time"] / data["iobound_burst_times"]) * 1000) / 1000   
        result["iobound_avg_wait_time"] = math.ceil(((data["iobound_turnaround_time"] / data["iobound_burst_times"])
                                                  - (data["iobound_cpu_burst_time"] / data["iobound_burst_times"]) - t_cs) * 1000) / 1000
        result["iobound_avg_turnaround_time"] = math.ceil((data["iobound_turnaround_time"] / data["iobound_burst_times"]) * 1000) / 1000

    result["context_switch"] = data["context_switch"]
    result["cpu_context_switch"] = data["cpu_context_switch"]
    result["io_context_switch"] = data["io_context_switch"]

    result["preemption"] = data["preemption"]
    result["cpu_preemption"] = data["cpu_preemption"]
    result["io_preemption"] = data["io_preemption"]

    return result

#calculate preemptive algo's result
def preemptive_result(data, result, t_cs):
    if data["time"] == 0:
        result["cpu_utilization"] = 0
    else:
         result["cpu_utilization"] = math.ceil(((data["total_cpu_elapsed_time"] / data["time"]) * 100) * 1000) / 1000

    if data["total_cpu_burst_times"] == 0:
        result["avg_cpu_burst_time"] = 0
        total_avg_context_switch = 0
        result["avg_turnaround_time"] = 0
        result["avg_wait_time"] = 0
    else:
        total_avg_context_switch = ((data["context_switch"] * t_cs) / data["total_cpu_burst_times"])
        result["avg_cpu_burst_time"] = math.ceil((data["total_cpu_elapsed_time"] / data["total_cpu_burst_times"]) * 1000) / 1000
        result["avg_turnaround_time"] = math.ceil((data["total_turnaround_time"] / data["total_cpu_burst_times"]) * 1000) / 1000
        result["avg_wait_time"] = math.ceil(((data["total_turnaround_time"] / data["total_cpu_burst_times"]) - (data["total_cpu_elapsed_time"]
                                                                                 / data["total_cpu_burst_times"]) - total_avg_context_switch) * 1000) / 1000

    if data["cpubound_burst_times"] == 0:
        cpubound_avg_context_switch = 0
        result["cpubound_avg_cpu_burst_time"] = 0
        result["cpubound_avg_wait_time"] = 0
        result["cpubound_avg_turnaround_time"] = 0
    else:
        cpubound_avg_context_switch = ((data["cpu_context_switch"] * t_cs) / data["cpubound_burst_times"])
        result["cpubound_avg_cpu_burst_time"] = math.ceil((data["cpubound_cpu_burst_time"] / data["cpubound_burst_times"]) * 1000) / 1000
        result["cpubound_avg_wait_time"] = math.ceil(((data["cpubound_turnaround_time"] / data["cpubound_burst_times"]) - 
                                                  (data["cpubound_cpu_burst_time"] / data["cpubound_burst_times"]) - cpubound_avg_context_switch) * 1000) / 1000
        result["cpubound_avg_turnaround_time"] = math.ceil((data["cpubound_turnaround_time"] / data["cpubound_burst_times"]) * 1000) / 1000

    if data["iobound_burst_times"] == 0:
        iobound_avg_context_switch = 0
        result["iobound_avg_cpu_burst_time"] = 0
        result["iobound_avg_wait_time"] = 0
        result["iobound_avg_turnaround_time"] = 0
    else:
        iobound_avg_context_switch = ((data["io_context_switch"] * t_cs) / data["iobound_burst_times"]) 
        result["iobound_avg_cpu_burst_time"] = math.ceil((data["iobound_cpu_burst_time"] / data["iobound_burst_times"]) * 1000) / 1000   
        result["iobound_avg_wait_time"] = math.ceil(((data["iobound_turnaround_time"] / data["iobound_burst_times"])
                                                  - (data["iobound_cpu_burst_time"] / data["iobound_burst_times"]) - iobound_avg_context_switch) * 1000) / 1000
        result["iobound_avg_turnaround_time"] = math.ceil((data["iobound_turnaround_time"] / data["iobound_burst_times"]) * 1000) / 1000

    result["context_switch"] = data["context_switch"]
    result["cpu_context_switch"] = data["cpu_context_switch"]
    result["io_context_switch"] = data["io_context_switch"]

    result["preemption"] = data["preemption"]
    result["cpu_preemption"] = data["cpu_preemption"]
    result["io_preemption"] = data["io_preemption"]

    return result

#Check if the input is valid
try:
    n = int(sys.argv[1])
    ncpu = int(sys.argv[2])
    seed = int(sys.argv[3])
    _lambda = float(sys.argv[4])
    upperLimit = int(sys.argv[5])
    t_cs = int(sys.argv[6])
    alpha = f32(sys.argv[7])
    t_slice = int(sys.argv[8])
except (IndexError, ValueError):
    print('ERROR: Usage: python3 project.py (number of process) (number of process bound with cpu) (random seed) (lambda) (upperLimit)', file=sys.stderr)
    sys.exit(1)

#Check if the input is in the valid range
if n < 0 or ncpu < 0 or upperLimit < 0 or alpha < 0:
    print("ERROR: Invalid input either number of processes(arg1), number of cpu-bound processes(arg2), upperLimit(arg5) or alpha number(arg7/range between 0 to 1) is negative please use positive integer", file=sys.stderr)
    sys.exit(1)

if ncpu > n:
    print("ERROR: Invalid input can't have cpu-bound process number(arg2) greater than total process number(arg1)", file=sys.stderr)
    sys.exit(1)

if alpha > 1:
    print("ERROR: Invalid input alpha number(arg7) is greater than 1 please use number between 0 and 1", file=sys.stderr)
    sys.exit(1)

#create random number generator
random = Rand48(seed, _lambda, upperLimit)

#determine if we add "es" to the end of the word "process"
es = ""
if ncpu != 1:
    es = "es"

print("<<< PROJECT PART I -- process set (n={}) with {} CPU-bound process{} >>>".format(n, ncpu, es))

process_list = []
#Below is the I/O bound process generator
for i in range(n-ncpu):
    arrival_time = random.floor()
    cpu_burst_times = math.trunc(random.drand() * 64)
    pid = chr(65 + i)

    cpu_burst_time = []
    io_burst_time = []
    p = Process(arrival_time, "I/O-bound", pid, _lambda)
    #put the CPU burst time and I/O burst time into the list
    for j in range(cpu_burst_times):
        cpu_burst_time.append(random.ceil())
        io_burst_time.append(random.ceil() * 10)
    cpu_burst_time.append(random.ceil())
    p.set_burst(cpu_burst_time, io_burst_time)
    process_list.append(p)

#Below is the CPU bound process generator
for i in range(n - ncpu, n):
    arrival_time = random.floor()
    cpu_burst_times = math.trunc(random.drand() * 64)
    pid = chr(65 + i)

    cpu_burst_time = []
    io_burst_time = []
    p = Process(arrival_time, "CPU-bound", pid, _lambda)
    #put the CPU burst time and I/O burst time into the list
    for j in range(cpu_burst_times):
        cpu_burst_time.append(random.ceil() * 4)
        io_burst_time.append(random.ceil() * 10 // 8)
    cpu_burst_time.append(random.ceil() * 4)
    p.set_burst(cpu_burst_time, io_burst_time)
    process_list.append(p)

for p in process_list:
    print(p)
print()   #for part 1 comment out this line
    
print("<<< PROJECT PART II -- t_cs={}ms; alpha={:.2f}; t_slice={}ms >>>".format(t_cs, alpha, t_slice))

#First-come-first-served (FCFS)
FCFS_data = FCFS(process_list, t_cs)
FCFS_result = deepcopy(result_template)

FCFS_result = non_preemptive_result(FCFS_data, FCFS_result, t_cs)

FCFS_text = (
        "Algorithm FCFS\n"
        "-- CPU utilization: {:.3f}%\n"
        "-- average CPU burst time: {:.3f} ms ({:.3f} ms/{:.3f} ms)\n"
        "-- average wait time: {:.3f} ms ({:.3f} ms/{:.3f} ms)\n"
        "-- average turnaround time: {:.3f} ms ({:.3f} ms/{:.3f} ms)\n"
        "-- number of context switches: {:.0f} ({:.0f}/{:.0f})\n"
        "-- number of preemptions: {} ({}/{})\n\n"
    ).format(FCFS_result["cpu_utilization"], 
             FCFS_result["avg_cpu_burst_time"], FCFS_result["cpubound_avg_cpu_burst_time"], FCFS_result["iobound_avg_cpu_burst_time"],
             FCFS_result["avg_wait_time"], FCFS_result["cpubound_avg_wait_time"], FCFS_result["iobound_avg_wait_time"],
             FCFS_result["avg_turnaround_time"], FCFS_result["cpubound_avg_turnaround_time"], FCFS_result["iobound_avg_turnaround_time"],
             FCFS_result["context_switch"], FCFS_result["cpu_context_switch"], FCFS_result["io_context_switch"],
             FCFS_result["preemption"], FCFS_result["cpu_preemption"], FCFS_result["io_preemption"])

#Shortest job first (SJF)
SJF_data = SJF(process_list, t_cs, alpha)
SJF_result = deepcopy(result_template)

SJF_result = non_preemptive_result(SJF_data, SJF_result, t_cs)

SJF_text = (
        "Algorithm SJF\n"
        "-- CPU utilization: {:.3f}%\n"
        "-- average CPU burst time: {:.3f} ms ({:.3f} ms/{:.3f} ms)\n"
        "-- average wait time: {:.3f} ms ({:.3f} ms/{:.3f} ms)\n"
        "-- average turnaround time: {:.3f} ms ({:.3f} ms/{:.3f} ms)\n"
        "-- number of context switches: {:.0f} ({:.0f}/{:.0f})\n"
        "-- number of preemptions: {} ({}/{})\n\n"
    ).format(SJF_result["cpu_utilization"],
             SJF_result["avg_cpu_burst_time"], SJF_result["cpubound_avg_cpu_burst_time"], SJF_result["iobound_avg_cpu_burst_time"],
             SJF_result["avg_wait_time"], SJF_result["cpubound_avg_wait_time"], SJF_result["iobound_avg_wait_time"],
             SJF_result["avg_turnaround_time"], SJF_result["cpubound_avg_turnaround_time"], SJF_result["iobound_avg_turnaround_time"],
             SJF_result["context_switch"], SJF_result["cpu_context_switch"], SJF_result["io_context_switch"],
             SJF_result["preemption"], SJF_result["cpu_preemption"], SJF_result["io_preemption"])


#Shortest remaining time (SRT)
SRT_data = SRT(process_list, t_cs, alpha)
SRT_result = deepcopy(result_template)

SRT_result = preemptive_result(SRT_data, SRT_result, t_cs)

SRT_text = (
        "Algorithm SRT\n"
        "-- CPU utilization: {:.3f}%\n"
        "-- average CPU burst time: {:.3f} ms ({:.3f} ms/{:.3f} ms)\n"
        "-- average wait time: {:.3f} ms ({:.3f} ms/{:.3f} ms)\n"
        "-- average turnaround time: {:.3f} ms ({:.3f} ms/{:.3f} ms)\n"
        "-- number of context switches: {:.0f} ({:.0f}/{:.0f})\n"
        "-- number of preemptions: {} ({}/{})\n\n"
    ).format(SRT_result["cpu_utilization"],
             SRT_result["avg_cpu_burst_time"], SRT_result["cpubound_avg_cpu_burst_time"], SRT_result["iobound_avg_cpu_burst_time"],
             SRT_result["avg_wait_time"], SRT_result["cpubound_avg_wait_time"], SRT_result["iobound_avg_wait_time"],
             SRT_result["avg_turnaround_time"], SRT_result["cpubound_avg_turnaround_time"], SRT_result["iobound_avg_turnaround_time"],
             SRT_result["context_switch"], SRT_result["cpu_context_switch"], SRT_result["io_context_switch"],
             SRT_result["preemption"], SRT_result["cpu_preemption"], SRT_result["io_preemption"])


#Round robin (RR)
RR_data = RR(process_list, t_cs, t_slice)
RR_result = deepcopy(result_template)

RR_result = preemptive_result(RR_data, RR_result, t_cs)

RR_text = (
        "Algorithm RR\n"
        "-- CPU utilization: {:.3f}%\n"
        "-- average CPU burst time: {:.3f} ms ({:.3f} ms/{:.3f} ms)\n"
        "-- average wait time: {:.3f} ms ({:.3f} ms/{:.3f} ms)\n"
        "-- average turnaround time: {:.3f} ms ({:.3f} ms/{:.3f} ms)\n"
        "-- number of context switches: {:.0f} ({:.0f}/{:.0f})\n"
        "-- number of preemptions: {} ({}/{})\n"
    ).format(RR_result["cpu_utilization"],
             RR_result["avg_cpu_burst_time"], RR_result["cpubound_avg_cpu_burst_time"], RR_result["iobound_avg_cpu_burst_time"],
             RR_result["avg_wait_time"], RR_result["cpubound_avg_wait_time"], RR_result["iobound_avg_wait_time"],
             RR_result["avg_turnaround_time"], RR_result["cpubound_avg_turnaround_time"], RR_result["iobound_avg_turnaround_time"],
             RR_result["context_switch"], RR_result["cpu_context_switch"], RR_result["io_context_switch"],
             RR_result["preemption"], RR_result["cpu_preemption"], RR_result["io_preemption"])

Final_output = FCFS_text + SJF_text + SRT_text + RR_text

with open('simout.txt', 'w') as file:
    # Write Final output to the file
    file.write(Final_output)