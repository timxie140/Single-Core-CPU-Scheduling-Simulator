from math import ceil
from numpy import float32 as f32
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
    result = (alpha * f32(burst_time)) + ((1 - alpha) * f32(old_tau))
    return ceil(f32(result))

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
            Q.append(io_p[index])
            Q.sort(key=lambda x: x.get_pid())
            Q.sort(key=lambda x: x.get_tau())
            if(cur_time<10000):
                print("time {}ms: Process {} (tau {}ms) completed I/O; added to ready queue {}".format(cur_time, io_p[index].get_pid(), io_p[index].get_tau(), print_ready_Q(Q)))
            io_p.pop(index)
    

def SJF(process_list, t_cs, alpha):
    half_t_cs = t_cs // 2
    cpu_p = None
    io_p = []

    arr_list = deepcopy(process_list)
    arr_list.sort(key=lambda x: x.get_arrival_time())

    print("time 0ms: Simulator started for SJF [Q <empty>]")

    living_p = len(process_list)
    Q = []
    cur_time = 0
    switchs = 0
    cpu_switchs = 0
    io_switchs = 0
    cpu_turn = {}
    io_turn = {}
    cpu_burst = 0
    io_burst = 0
    cpu_burst_times = 0
    cpubound_cpu_burst_times = 0
    iobound_cpu_burst_times = 0
    cpubound_cpu_burst_time = 0
    iobound_cpu_burst_time = 0
    cpubound_io_burst_time = 0
    iobound_io_burst_time = 0
    for p in arr_list:
        io_burst += p.get_sum_io_burst()
        cpu_burst += p.get_sum_cpu_burst()
        cpu_burst_times += p.get_cpu_burst_times()
        if p.get_ID() == "CPU-bound":
            cpubound_cpu_burst_times += p.get_cpu_burst_times()
            cpubound_cpu_burst_time += p.get_sum_cpu_burst()
            cpubound_io_burst_time += p.get_sum_io_burst()
        else:
            iobound_cpu_burst_times += p.get_cpu_burst_times()
            iobound_cpu_burst_time += p.get_sum_cpu_burst()
            iobound_io_burst_time += p.get_sum_io_burst()
    context_status = 0 
    context_count = 0 
    cpu_using_context = 0
    cpu_p_wait_for_context  = None

    while(living_p!= 0):
        #CPU_PART
        if len(arr_list) != 0:
            if arr_list[0].get_arrival_time() == cur_time:
                arr_list[0].set_turnaround_start(cur_time)  #set start of turnaround time 
                Q.append(arr_list[0])
                Q.sort(key=lambda x: x.get_pid())
                Q.sort(key=lambda x: x.get_tau())
                if(cur_time<10000):
                    print("time {}ms: Process {} (tau {}ms) arrived; added to ready queue {}".format(cur_time,arr_list[0].get_pid(),arr_list[0].get_tau(),print_ready_Q(Q)))
                arr_list.pop(0)
                continue
        if context_status !=1:
            if cpu_p != None:
                if cur_time == cpu_p.get_cpu_burst_stop_time():
                    if cpu_p.get_cpu_burst_times()-1 != 0:
                        if cur_time<10000:
                            if (cpu_p.get_cpu_burst_times()-1)>1 :
                                print("time {}ms: Process {} (tau {}ms) completed a CPU burst; {} bursts to go {}".format(cur_time, cpu_p.get_pid(), cpu_p.get_tau(), cpu_p.get_cpu_burst_times()-1, print_ready_Q(Q)))
                            else:
                                print("time {}ms: Process {} (tau {}ms) completed a CPU burst; {} burst to go {}".format(cur_time, cpu_p.get_pid(), cpu_p.get_tau(), cpu_p.get_cpu_burst_times()-1, print_ready_Q(Q)))

                    elif cpu_p.get_cpu_burst_times()-1 == 0:
                        cpu_p.change_cpu_burst()
                        print("time {}ms: Process {} terminated {}".format(cur_time, cpu_p.get_pid(), print_ready_Q(Q)))
                        living_p -= 1
                        cpu_p.set_turnaround_end(cur_time + half_t_cs)
                        cpu_p.cal_turnaround_time()
                        if(cpu_p.get_ID() == "CPU-bound"):
                            cpu_switchs+=0.5
                            cpu_turn[cpu_p.get_pid()] =  cpu_p.get_turnaround_time()
                        else:
                            io_switchs+=0.5
                            io_turn[cpu_p.get_pid()] = cpu_p.get_turnaround_time()
                        switchs+=0.5
                        cpu_p = None
                        context_status = 1
                        context_count = half_t_cs
                        
                        continue

                    
                    if(cur_time<10000):
                        print("time {}ms: Recalculating tau for process {}: old tau {}ms ==> new tau {}ms {}".format(cur_time, cpu_p.get_pid(), cpu_p.get_tau(), find_new_tau(alpha,cpu_p.get_tau(),cpu_p.get_cpu_burst_time(0)), print_ready_Q(Q)))
                    cpu_p.set_tau(find_new_tau(alpha,cpu_p.get_tau(),cpu_p.get_cpu_burst_time(0)))
                    cpu_p.change_cpu_burst()
                    cpu_p.set_io_burst_stop_time(cur_time+half_t_cs+cpu_p.get_io_burst_time(0))
                    io_p.append(cpu_p)
                    io_p.sort(key=lambda x: x.get_pid())
                    io_p.sort(key=lambda x: x.get_io_burst_stop_time())
                    if(cur_time<10000):
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

                        context_status = 1
                        cpu_using_context = 1
                        context_count = half_t_cs
                        continue
                    elif context_status == 2:
                        context_status = 0
                        cpu_using_context = 0
                        cpu_p = cpu_p_wait_for_context
                        cpu_p_wait_for_context = None
                        if(cur_time<10000):
                            print("time {}ms: Process {} (tau {}ms) started using the CPU for {}ms burst {}".format(cur_time, cpu_p.get_pid(), cpu_p.get_tau(), cpu_p.get_cpu_burst_time(0), print_ready_Q(Q)))
                        cpu_p.set_cpu_burst_stop_time(cur_time + cpu_p.get_cpu_burst_time(0))
                        
                        if(cpu_p.get_ID() == "CPU-bound"):
                            cpu_switchs+=0.5
                        else:
                            io_switchs+=0.5

                        switchs+=0.5
        else:
            context_count -= 1
            if context_count == 0 and cpu_using_context == 1:
                context_status = 2
            elif context_count == 0:
                context_status = 0

        #IO_PART
        if len(io_p)!=0:
            while find_complete_IO(cur_time, io_p)!= -1:
                index = find_complete_IO(cur_time, io_p)
                io_p[index].change_io_burst()
                Q.append(io_p[index])
                Q.sort(key=lambda x: x.get_pid())
                Q.sort(key=lambda x: x.get_tau())
                if(cur_time<10000):
                    print("time {}ms: Process {} (tau {}ms) completed I/O; added to ready queue {}".format(cur_time, io_p[index].get_pid(), io_p[index].get_tau(), print_ready_Q(Q)))
                
                io_p.pop(index)
                
        cur_time += 1

    if context_status == 1:
        cur_time+=half_t_cs

    print("time {}ms: Simulator ended for SJF [Q <empty>]\n".format(cur_time))

    total_turn_time = sum(cpu_turn.values())+sum(io_turn.values()) - io_burst
    cpubound_turn_time = sum(cpu_turn.values()) - cpubound_io_burst_time
    iobound_turn_time = sum(io_turn.values()) - iobound_io_burst_time

    SJF_Dictionary = {"time": cur_time,
                     "total_cpu_elapsed_time": cpu_burst, 
                     "total_cpu_burst_times": cpu_burst_times, 
                     "cpubound_cpu_burst_time": cpubound_cpu_burst_time,
                     "iobound_cpu_burst_time": iobound_cpu_burst_time,
                     "cpubound_burst_times": cpubound_cpu_burst_times,
                     "iobound_burst_times": iobound_cpu_burst_times,
                     "total_turnaround_time": total_turn_time,
                     "iobound_turnaround_time": iobound_turn_time,
                     "cpubound_turnaround_time": cpubound_turn_time,
                     "context_switch": switchs,
                     "cpu_context_switch": cpu_switchs,
                     "io_context_switch": io_switchs,
                     "preemption": 0,
                     "io_preemption": 0,
                     "cpu_preemption": 0,}

    return SJF_Dictionary
