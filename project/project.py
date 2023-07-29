import sys
import math
from drand48 import Rand48
from process import Process
from copy import deepcopy

def print_ready_Q(ready_Q):
    if len(ready_Q) != 0:
        text = "[Q"
        for p in ready_Q:
            text += " {}".format(p.pid)
        text += "]"
    else:
        text = "[Q <empty>]"
    return text

#Check if the input is valid
try:
    n = int(sys.argv[1])
    ncpu = int(sys.argv[2])
    seed = int(sys.argv[3])
    _lambda = float(sys.argv[4])
    upperLimit = int(sys.argv[5])
    t_cs = int(sys.argv[6])
    alpha = float(sys.argv[7])
    t_slice = int(sys.argv[8])
except (IndexError, ValueError):
    print("Usage: python3 project.py (number of process) (number of process bound with cpu) (random seed) (lambda) (upperLimit)")
    sys.exit(1)

#Check if the input is in the valid range
if n < 0 or ncpu < 0 or upperLimit < 0:
    print("Error: Invalid input either n, ncpu or upperLimit is negative please use positive integer")
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
    p = Process(arrival_time, "I/O-bound", pid)
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
    p = Process(arrival_time, "CPU-bound", pid)
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
    
print("<<< PROJECT PART II -- t_cs={}ms; alpha={}; t_slice={}ms >>>".format(t_cs, alpha, t_slice))
time = 0
half_t_cs = t_cs // 2
ready_Q = []
RUNNING = 0
cpu_p = None
io_p = None

#First-come-first-served (FCFS)
FCFS_process_list = deepcopy(process_list)
FCFS_process_list.sort(key=lambda x: x.get_arrival_time())
alive_process = len(process_list)

total_io_elapsed_time = 0
total_cpu_elapsed_time = 0
context_switch = 0

Finished_list = []

for p in FCFS_process_list:
    total_io_elapsed_time += p.get_sum_io_burst()
    total_cpu_elapsed_time += p.get_sum_cpu_burst()

print("time {}ms: Simulator started for FCFS {}".format(time, print_ready_Q(ready_Q)))

while alive_process != 0:
    if len(FCFS_process_list) != 0 and FCFS_process_list[0].get_arrival_time() == time:
        p = FCFS_process_list.pop(0)
        ready_Q.append(p)
        p.set_turnaround_start(time)
        p.set_wait_start(time)
        if time < 9999:
            print("time {}ms: Process {} arrived; added to ready queue {}".format(time, p.get_pid(), print_ready_Q(ready_Q)))
        
    if RUNNING == 0 and len(ready_Q) != 0:
        cpu_p = ready_Q.pop(0)
        cpu_p.set_wait_end(time)
        cpu_p.cal_wait_time()
        time += half_t_cs
        RUNNING = 1
        cpu_p.set_cpu_burst_stop_time(cpu_p.get_cpu_burst_time(0) + time)
        if time < 9999:
            print("time {}ms: Process {} started using the CPU for {}ms burst {}".format(time, cpu_p.get_pid(), cpu_p.get_cpu_burst_time(0), print_ready_Q(ready_Q)))
        context_switch += 1
        
    if RUNNING == 1 and cpu_p.get_cpu_burst_stop_time() == time:
        cpu_p.change_cpu_burst()
        RUNNING = 0
        io_p = cpu_p
        cpu_p = None
        if time < 9999:
            print("time {}ms: Process {} completed a CPU burst; {} bursts to go {}".format(time, io_p.get_pid(), io_p.get_cpu_burst_times(), print_ready_Q(ready_Q)))
        if io_p.get_cpu_burst_times() == 0:
            io_p.set_turnaround_end(time)
            io_p.cal_turnaround_time()
            Finished_list.append(io_p)
            print("time {}ms: Process {} terminated {}".format(time, io_p.get_pid(), print_ready_Q(ready_Q)))
            alive_process -= 1
            io_p = None
        else:
            io_p.set_io_burst_stop_time(io_p.get_io_burst_time(0) + time + half_t_cs)
            if time < 9999:
                print("time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms {}".format(time, io_p.get_pid(), io_p.get_io_burst_stop_time(), print_ready_Q(ready_Q)))
        time += half_t_cs
        time -= 1
    
    if io_p != None and io_p.get_io_burst_stop_time() == time:
        ready_Q.append(io_p)    
        io_p.change_io_burst()
        if time < 9999:
            print("time {}ms: Process {} completed I/O; added to ready queue {}".format(time, io_p.get_pid(), print_ready_Q(ready_Q)))
        io_p.set_wait_start(time)
        
    time += 1
    if time % 100000 == 0:
        print(cpu_p.getpid())

print("CPU Utilization: {}".format(total_cpu_elapsed_time / time))

#Shortest job first (SJF)



#Shortest remaining time (SRT)



#Round robin (RR)