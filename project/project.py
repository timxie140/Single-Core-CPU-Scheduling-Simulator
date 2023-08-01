import sys
import math
from drand48 import Rand48
from process import Process
from FCFS import FCFS
from RR import RR

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
FCFS_output = FCFS(process_list, t_cs)

#Shortest job first (SJF)



#Shortest remaining time (SRT)



#Round robin (RR)
RR_output = RR(process_list, t_cs, t_slice)

Final_output = FCFS_output + RR_output

with open('project/simout.txt', 'w') as file:
    # Write Final output to the file
    file.write(Final_output)