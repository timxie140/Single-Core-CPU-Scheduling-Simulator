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

def find_shortest_tau(Q):
    mini = float('inf')
    process_index = 0
    for i in range(len(Q)):
        if Q[i].get_tau() < mini:
            mini = Q[i].get_tau()
            process_index = i
    return process_index

def find_new_tau(alpha, old_tau, burst_time):
    result = (alpha * burst_time) + ((1-alpha) * old_tau)
    return math.ceil(result)

def find_complete_IO(time, io_p):
    index = -1
    for i in range(len(io_p)):
        if io_p[i].get_io_burst_stop_time() == time:
            index = i
    return index

def io_process(io_p, cur_time, Q):
    if len(io_p)!=0:
        if find_complete_IO(cur_time, io_p)!= -1:
            index = find_complete_IO(cur_time, io_p)
            io_p[index].change_io_burst()
            io_p[index].set_wait_start(cur_time)
            Q.append(io_p[index])
            Q.sort(key=lambda x: x.get_pid())
            Q.sort(key=lambda x: x.get_tau())
            if(cur_time<10000):
                print("time {}ms: Process {} (tau {}ms) completed I/O; added to ready queue {}".format(cur_time, io_p[index].get_pid(), io_p[index].get_tau(), print_ready_Q(Q)))
            io_p.pop(index)
    
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
io_p = []

arr_list = []
for p in process_list:
    arr_list.append(p)

arr_list.sort(key=lambda x: x.get_arrival_time())

print("time 0ms: Simulator started for SJF [Q <empty>]")

living_p = len(process_list)
Q = []
cur_time = 0
switchs = 0
cpu_switchs = 0
io_switchs = 0
cpu_wait = {}
io_wait = {}
cpu_turn = {}
io_turn = {}
io_burst = {}
cpu_burst = sum(i.get_sum_cpu_burst() for i in process_list)

while(living_p!= 0):
    #CPU_PART
    if len(arr_list) != 0:
        if arr_list[0].get_arrival_time() == cur_time:
            arr_list[0].set_wait_start(cur_time)    #set start of wait time
            arr_list[0].set_turnaround_start(cur_time)  #set start of turnaround time 
            io_burst[arr_list[0].get_pid()] = arr_list[0].get_sum_io_burst()
            Q.append(arr_list[0])
            Q.sort(key=lambda x: x.get_pid())
            Q.sort(key=lambda x: x.get_tau())
            if(cur_time<10000):
                print("time {}ms: Process {} (tau {}ms) arrived; added to ready queue {}".format(cur_time,arr_list[0].get_pid(),arr_list[0].get_tau(),print_ready_Q(Q)))
            arr_list.pop(0)
            continue

    if cpu_p != None:
        if cur_time == cpu_p.get_cpu_burst_stop_time():
            if(cur_time<10000):
                print("time {}ms: Process {} (tau {}ms) completed a CPU burst; {} bursts to go {}".format(cur_time, cpu_p.get_pid(), cpu_p.get_tau(), cpu_p.get_cpu_burst_times()-1, print_ready_Q(Q)))
            if cpu_p.get_cpu_burst_times()-1 == 0:
                cpu_p.change_cpu_burst()
                print("time {}ms: Process {} terminated {}".format(cur_time, cpu_p.get_pid(), print_ready_Q(Q)))
                living_p -= 1
                cpu_p.set_turnaround_end(cur_time + half_t_cs)
                cpu_p.cal_turnaround_time()
                if(cpu_p.get_ID() == "CPU-bound"):
                    cpu_switchs+=0.5
                    cpu_turn[cpu_p.get_pid()] =  cpu_p.get_turnaround_time() - io_burst[cpu_p.get_pid()]
                else:
                    io_switchs+=0.5
                    io_turn[cpu_p.get_pid()] = cpu_p.get_turnaround_time() - io_burst[cpu_p.get_pid()]

                cpu_p = None
                for i in range(half_t_cs+1):
                    io_process(io_p,cur_time+i, Q)
                cur_time += half_t_cs
                switchs+=0.5
                continue

            if(find_new_tau(alpha,cpu_p.get_tau(),cpu_p.get_cpu_burst_time(0))!= cpu_p.get_tau()):
                if(cur_time<10000):
                    print("time {}ms: Recalculating tau for process {}: old tau {}ms ==> new tau {}ms {}".format(cur_time, cpu_p.get_pid(), cpu_p.get_tau(), find_new_tau(alpha,cpu_p.get_tau(),cpu_p.get_cpu_burst_time(0)), print_ready_Q(Q)))
                cpu_p.set_tau(find_new_tau(alpha,cpu_p.get_tau(),cpu_p.get_cpu_burst_time(0)))
            cpu_p.change_cpu_burst()
            cpu_p.set_io_burst_stop_time(cur_time+half_t_cs+cpu_p.get_io_burst_time(0))
            io_p.append(cpu_p)
            if(cur_time<10000):
                print("time {}ms: Process {} switching out of CPU; blocking on I/O until time {}ms {}".format(cur_time, cpu_p.get_pid(), cpu_p.get_io_burst_stop_time(), print_ready_Q(Q)))
            
            if(cpu_p.get_ID() == "CPU-bound"):
                cpu_switchs+=0.5
            else:
                io_switchs+=0.5

            cpu_p = None
            for i in range(half_t_cs+1):
                io_process(io_p,cur_time+i, Q)
            cur_time += half_t_cs
            switchs+=0.5
            continue

    elif(len(Q)!=0):
        #index  = find_shortest_tau(Q)
        cpu_p = Q[0]
        Q.pop(0)
        if(cur_time<10000):
            print("time {}ms: Process {} (tau {}ms) started using the CPU for {}ms burst {}".format(cur_time + half_t_cs, cpu_p.get_pid(), cpu_p.get_tau(), cpu_p.get_cpu_burst_time(0), print_ready_Q(Q)))

        cpu_p.set_wait_end(cur_time)
        cpu_p.set_cpu_burst_stop_time(cur_time + half_t_cs + cpu_p.get_cpu_burst_time(0))

        if(cpu_p.get_ID() == "CPU-bound"):
            cpu_switchs+=0.5
            cpu_p.cal_wait_time()
            cpu_wait[cpu_p.get_pid()] = cpu_p.get_wait_time()
        else:
            io_switchs+=0.5
            cpu_p.cal_wait_time()
            io_wait[cpu_p.get_pid()] = cpu_p.get_wait_time()

        for i in range(half_t_cs):
            io_process(io_p,cur_time+1+i, Q)
        cur_time += half_t_cs
        switchs+=0.5
    

    #IO_PART
    if len(io_p)!=0:
        if find_complete_IO(cur_time, io_p)!= -1:
            index = find_complete_IO(cur_time, io_p)
            io_p[index].change_io_burst()
            io_p[index].set_wait_start(cur_time)
            Q.append(io_p[index])
            Q.sort(key=lambda x: x.get_pid())
            Q.sort(key=lambda x: x.get_tau())
            if(cur_time<10000):
                print("time {}ms: Process {} (tau {}ms) completed I/O; added to ready queue {}".format(cur_time, io_p[index].get_pid(), io_p[index].get_tau(), print_ready_Q(Q)))
            
            io_p.pop(index)
            continue
    cur_time += 1


print("time {}ms: Simulator ended for SJF [Q <empty>]".format(cur_time))
print(switchs)
print(cpu_switchs)
print(io_switchs)
print((sum(cpu_wait.values())+sum(io_wait.values()))/switchs)
print(sum(cpu_wait.values())/cpu_switchs)
print(sum(io_wait.values())/io_switchs)
print((sum(cpu_turn.values())+sum(io_turn.values()))/switchs)
print(sum(cpu_turn.values())/cpu_switchs)
print(sum(io_turn.values())/io_switchs)
print(cpu_burst/cur_time)
