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

arr_list = []
for p in process_list:
    arr_list.append(p)

arr_list.sort(key=lambda x: x.get_arrival_time())

print("time 0ms: Simulator started for SJF [Q <empty>]")

living_p = len(process_list)
while(living_p!= 0):
    


