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
            break
    return index

def io_process(io_p, cur_time, Q):
    if len(io_p)!=0:
        while find_complete_IO(cur_time, io_p)!= -1:
            index = find_complete_IO(cur_time, io_p)
            io_p[index].change_io_burst()
            io_p[index].set_wait_start(cur_time)
            Q.append(io_p[index])
            Q.sort(key=lambda x: x.get_pid())
            Q.sort(key=lambda x: x.get_predict_time())
            #if(cur_time<10000):
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

print("time 0ms: Simulator started for SRT [Q <empty>]")

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
context_status = 0 
context_count = 0 
cpu_using_context = 0
cpu_p_wait_for_context  = None
preemp = 0
cpu_preemp = 0
io_preemp = 0
burst_times = 0
cpu_B_burst_times = 0
io_B_burst_times = 0
while(living_p!= 0):
    #ARR_PART
    if len(arr_list) != 0:
        if arr_list[0].get_arrival_time() == cur_time:
            arr_list[0].set_wait_start(cur_time)    #set start of wait time
            arr_list[0].set_turnaround_start(cur_time)  #set start of turnaround time 
            io_burst[arr_list[0].get_pid()] = arr_list[0].get_sum_io_burst()
            Q.append(arr_list[0])
            Q.sort(key=lambda x: x.get_pid())
            Q.sort(key=lambda x: x.get_predict_time())

            burst_times+=arr_list[0].get_cpu_burst_times()
            if arr_list[0].get_ID() == "CPU-bound":
                cpu_B_burst_times+=arr_list[0].get_cpu_burst_times()
            else:
                io_B_burst_times+=arr_list[0].get_cpu_burst_times()
            #if(cur_time<10000):
            print("time {}ms: Process {} (tau {}ms) arrived; added to ready queue {}".format(cur_time,arr_list[0].get_pid(),arr_list[0].get_tau(),print_ready_Q(Q)))
            arr_list.pop(0)
            continue
    #CPU_PART
    if context_status != 1:
        if cpu_p != None:
            if cur_time == cpu_p.get_cpu_burst_stop_time():
                #Complete or not
                if cpu_p.get_cpu_burst_times()-1 != 0:
                #if(cur_time<10000):
                    if (cpu_p.get_cpu_burst_times()-1)>1 :
                        print("time {}ms: Process {} (tau {}ms) completed a CPU burst; {} bursts to go {}".format(cur_time, cpu_p.get_pid(), cpu_p.get_tau(), cpu_p.get_cpu_burst_times()-1, print_ready_Q(Q)))
                    else:
                        print("time {}ms: Process {} (tau {}ms) completed a CPU burst; {} burst to go {}".format(cur_time, cpu_p.get_pid(), cpu_p.get_tau(), cpu_p.get_cpu_burst_times()-1, print_ready_Q(Q)))
                    cpu_p.set_remaining_time(-1)

                elif cpu_p.get_cpu_burst_times()-1 == 0:
                    cpu_p.set_remaining_time(-1)
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

                    switchs+=0.5
                    cpu_p = None
                    #Doing IO when context switch
                    context_status = 1
                    context_count = half_t_cs
                    continue

                #if(cur_time<10000):
                print("time {}ms: Recalculating tau for process {}: old tau {}ms ==> new tau {}ms {}".format(cur_time, cpu_p.get_pid(), cpu_p.get_tau(), find_new_tau(alpha,cpu_p.get_tau(),cpu_p.get_cpu_burst_time(0)), print_ready_Q(Q)))
                cpu_p.set_tau(find_new_tau(alpha,cpu_p.get_tau(),cpu_p.get_cpu_burst_time(0)))

                cpu_p.change_cpu_burst()
                cpu_p.set_io_burst_stop_time(cur_time+half_t_cs+cpu_p.get_io_burst_time(0))
                io_p.append(cpu_p)
                io_p.sort(key=lambda x: x.get_pid())
                io_p.sort(key=lambda x: x.get_io_burst_stop_time())
                #if(cur_time<10000):
                print("time {}ms: Process {} switching out of CPU; blocking on I/O until time {}ms {}".format(cur_time, cpu_p.get_pid(), cpu_p.get_io_burst_stop_time(), print_ready_Q(Q)))
                
                if(cpu_p.get_ID() == "CPU-bound"):
                    cpu_switchs+=0.5
                else:
                    io_switchs+=0.5

                switchs+=0.5
                cpu_p = None
                #Doing IO when context switch
                context_status = 1
                context_count = half_t_cs
                continue

        else:
            #index  = find_shortest_tau(Q)
            if context_status !=2:
                io_process(io_p,cur_time, Q)

            if len(Q)!=0 or cpu_p_wait_for_context!=None:
                if context_status == 0 :
                    cpu_p_wait_for_context = Q[0]
                    Q.pop(0)
                    cpu_p_wait_for_context.set_wait_end(cur_time)
                    cpu_p_wait_for_context.cal_wait_time()
                    context_status = 1
                    cpu_using_context = 1
                    context_count = half_t_cs
                    continue
                elif context_status == 2:
                    context_status = 0
                    cpu_using_context = 0
                    cpu_p = cpu_p_wait_for_context
                    cpu_p_wait_for_context = None
                    #if(cur_time<10000):
                    if cpu_p.get_remaining_time() == -1:
                        print("time {}ms: Process {} (tau {}ms) started using the CPU for {}ms burst {}".format(cur_time, cpu_p.get_pid(), cpu_p.get_tau(), cpu_p.get_cpu_burst_time(0), print_ready_Q(Q)))
                        cpu_p.set_cpu_burst_stop_time(cur_time + cpu_p.get_cpu_burst_time(0))
                        cpu_p.set_predict_cpu_burst_stop_time(cur_time)
                    else:
                        print("time {}ms: Process {} (tau {}ms) started using the CPU for remaining {}ms of {}ms burst {}".format(cur_time, cpu_p.get_pid(), cpu_p.get_tau(), cpu_p.get_remaining_time(), cpu_p.get_cpu_burst_time(0), print_ready_Q(Q)))
                        cpu_p.set_cpu_burst_stop_time(cur_time + cpu_p.get_remaining_time())
                        cpu_p.set_fake_predict_cpu_burst_stop_time(cur_time)
                    
                    if(cpu_p.get_ID() == "CPU-bound"):
                        cpu_switchs+=0.5
                        cpu_wait[cpu_p.get_pid()] = cpu_p.get_wait_time()
                    else:
                        io_switchs+=0.5
                        io_wait[cpu_p.get_pid()] = cpu_p.get_wait_time()

                    switchs+=0.5

    #During Context switch 
    else:
        context_count -= 1
        if context_count == 0 and cpu_using_context == 1:
            context_status = 2
        elif context_count == 0:
            context_status = 0
    

    #Spcial preempting
    if cpu_p != None and len(Q)!=0 and Q[0].get_tau() < cpu_p.get_remain_predict_time(cur_time) and cpu_using_context == 0:
        Q[0].set_wait_start(cur_time)
        print("time {}ms: Process {} (tau {}ms) will preempt {} {}".format(cur_time, Q[0].get_pid(), Q[0].get_tau(), cpu_p.get_pid(), print_ready_Q(Q)))
        preemp+=1
        #old switch out
        cpu_p.set_wait_start(cur_time+half_t_cs)
        if cpu_p.get_cpu_burst_stop_time()-cur_time != cpu_p.get_cpu_burst_time(0):
            cpu_p.set_remaining_time(cpu_p.get_cpu_burst_stop_time()-cur_time)
        else:
            cpu_p.set_remaining_time(-1)
        Q.append(cpu_p)
        Q.sort(key=lambda x: x.get_pid())
        Q.sort(key=lambda x: x.get_predict_time())

        if(cpu_p.get_ID() == "CPU-bound"):
            cpu_switchs+=0.5
            cpu_preemp += 1
        else:
            io_switchs+=0.5
            io_preemp += 1
        

        cpu_p = Q[0]
        Q.pop(0)

        for i in range(half_t_cs):
            io_process(io_p,cur_time+i, Q)

        #new switch in
        cpu_p.set_wait_end(cur_time+half_t_cs)
        cpu_p.set_cpu_burst_stop_time(cur_time + t_cs + cpu_p.get_cpu_burst_time(0))
        cpu_p.set_predict_cpu_burst_stop_time(cur_time + t_cs)
        cpu_p.cal_wait_time()

        print("time {}ms: Process {} (tau {}ms) started using the CPU for {}ms burst {}".format(cur_time+t_cs, cpu_p.get_pid(), cpu_p.get_tau(), cpu_p.get_cpu_burst_time(0), print_ready_Q(Q)))
        if(cpu_p.get_ID() == "CPU-bound"):
            cpu_switchs+=0.5
            cpu_wait[cpu_p.get_pid()] = cpu_p.get_wait_time()
        else:
            io_switchs+=0.5
            io_wait[cpu_p.get_pid()] = cpu_p.get_wait_time()

        for i in range(half_t_cs):
            io_process(io_p,cur_time+half_t_cs+i, Q)
            
        switchs+=1
        cur_time += t_cs
        continue

    #IO_PART
    if len(io_p)!=0:
        while find_complete_IO(cur_time, io_p)!= -1:
            index = find_complete_IO(cur_time, io_p)
            io_p[index].change_io_burst()
            io_p[index].set_wait_start(cur_time)

            if cpu_p != None and io_p[index].get_tau() < cpu_p.get_remain_predict_time(cur_time) and cpu_using_context == 0:
                Q.append(io_p[index])
                Q.sort(key=lambda x: x.get_pid())
                Q.sort(key=lambda x: x.get_predict_time())
                print("time {}ms: Process {} (tau {}ms) completed I/O; preempting {} {}".format(cur_time, io_p[index].get_pid(), io_p[index].get_tau(), cpu_p.get_pid(), print_ready_Q(Q)))
                preemp+=1
                #old switch out
                cpu_p.set_wait_start(cur_time+half_t_cs)
                if cpu_p.get_cpu_burst_stop_time()-cur_time != cpu_p.get_cpu_burst_time(0):
                    cpu_p.set_remaining_time(cpu_p.get_cpu_burst_stop_time()-cur_time)
                else:
                    cpu_p.set_remaining_time(-1)
                

                if(cpu_p.get_ID() == "CPU-bound"):
                    cpu_switchs+=0.5
                    cpu_preemp += 1
                else:
                    io_switchs+=0.5
                    io_preemp += 1
                
                io_p.pop(index)

                for i in range(half_t_cs):
                    io_process(io_p,cur_time+i, Q)

                
                #new switch in
                Q.append(cpu_p)
                Q.sort(key=lambda x: x.get_pid())
                Q.sort(key=lambda x: x.get_predict_time())

                io_process(io_p, cur_time+half_t_cs, Q)

                cpu_p = Q[0]
                Q.pop(0)

                cpu_p.set_wait_end(cur_time+half_t_cs)
                cpu_p.set_cpu_burst_stop_time(cur_time + t_cs + cpu_p.get_cpu_burst_time(0))
                cpu_p.set_predict_cpu_burst_stop_time(cur_time + t_cs)
                cpu_p.cal_wait_time()

                for i in range(half_t_cs-1):
                    io_process(io_p, cur_time+half_t_cs+1+i, Q)

                print("time {}ms: Process {} (tau {}ms) started using the CPU for {}ms burst {}".format(cur_time+t_cs, cpu_p.get_pid(), cpu_p.get_tau(), cpu_p.get_cpu_burst_time(0), print_ready_Q(Q)))
                if(cpu_p.get_ID() == "CPU-bound"):
                    cpu_switchs+=0.5
                    cpu_wait[cpu_p.get_pid()] = cpu_p.get_wait_time()
                else:
                    io_switchs+=0.5
                    io_wait[cpu_p.get_pid()] = cpu_p.get_wait_time()

                    
                switchs+=1
                cur_time += t_cs
                continue

            else:
                Q.append(io_p[index])
                Q.sort(key=lambda x: x.get_pid())
                Q.sort(key=lambda x: x.get_predict_time())
                #if(cur_time<10000):
                print("time {}ms: Process {} (tau {}ms) completed I/O; added to ready queue {}".format(cur_time, io_p[index].get_pid(), io_p[index].get_tau(), print_ready_Q(Q)))
                
                io_p.pop(index)

    cur_time += 1

if context_status == 1:
    cur_time+=half_t_cs

print("time {}ms: Simulator ended for SRT [Q <empty>]".format(cur_time))
print(switchs)
print(cpu_switchs)
print(io_switchs)
# print((sum(cpu_wait.values())+sum(io_wait.values()))/switchs)
# print(sum(cpu_wait.values())/cpu_switchs)
# print(sum(io_wait.values())/io_switchs)
print((sum(cpu_turn.values())+sum(io_turn.values()))/burst_times)
print(sum(cpu_turn.values())/cpu_B_burst_times)
print(sum(io_turn.values())/io_B_burst_times)
# print(cpu_burst/cur_time)
# print(preemp)
# print(cpu_preemp)
# print(io_preemp)