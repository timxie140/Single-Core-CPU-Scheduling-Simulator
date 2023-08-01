from copy import deepcopy
import math

#function to print out the ready queue
def print_ready_Q(ready_Q):
    if len(ready_Q) != 0:
        text = "[Q"
        for p in ready_Q:
            text += " {}".format(p.pid)
        text += "]"
    else:
        text = "[Q <empty>]"
    return text

#RR is just a FCFS with a time slice, so there's changes in the code below 
#and will be highlighted with comments
def RR (process_list, t_cs, t_slice):
    #Below is the variables used in the algo
    time = 0
    half_t_cs = t_cs // 2
    ready_Q = []
    RUNNING = 0
    cpu_p = None
    io_p = None
    io_list = []
    RR_process_list = deepcopy(process_list)
    RR_process_list.sort(key=lambda x: x.get_arrival_time())
    alive_process = len(process_list)

    #Below is the variables used to calculate the data
    rr_total_cpu_burst_times = 0
    rr_total_cpu_elapsed_time = 0
    rr_total_io_elapsed_time = 0

    context_switch = 0
    io_context_switch = 0
    cpu_context_switch = 0

    CTX = 0
    CTX_stop_time = -1

    preem_ready_q_p = None

    iobound_burst_times = 0
    cpubound_burst_times = 0

    rr_iobound_cpu_burst_time = 0
    rr_cpubound_cpu_burst_time = 0
    rr_iobound_io_burst_time = 0
    rr_cpubound_io_burst_time = 0

    preemption = 0
    io_preemption = 0  
    cpu_preemption = 0

    #Below is the list of finished process
    Finished_list = []

    #Using for loop to prerecord the data that will not be available after the RR runs
    for p in RR_process_list:
        rr_total_cpu_elapsed_time += p.get_sum_cpu_burst()
        rr_total_cpu_burst_times += p.get_cpu_burst_times()
        rr_total_io_elapsed_time += p.get_sum_io_burst()
        if p.get_ID() == "I/O-bound":
            iobound_burst_times += p.get_cpu_burst_times()
            rr_iobound_cpu_burst_time += p.get_sum_cpu_burst()
            rr_iobound_io_burst_time += p.get_sum_io_burst()
        else:
            cpubound_burst_times += p.get_cpu_burst_times()
            rr_cpubound_cpu_burst_time += p.get_sum_cpu_burst()
            rr_cpubound_io_burst_time += p.get_sum_io_burst()

    #Starting the RR
    print("time {}ms: Simulator started for RR {}".format(time, print_ready_Q(ready_Q)))

    #RR algo runs here
    while alive_process != 0 or CTX != 0:
        if CTX_stop_time == time:
            if CTX == 2:        #If the process is terminated
                #Set the turnaround end time and calculate the turnaround time
                Finished_list[-1].set_turnaround_end(time)
                Finished_list[-1].cal_turnaround_time()
            CTX = 0
            if RUNNING == 0 and cpu_p != None:
                CTX_stop_time = -2      #Means this is the process cpu burst start context switch
            elif preem_ready_q_p != None:
                CTX_stop_time = -3      #Means this is the process preemption context switch
                ready_Q.append(preem_ready_q_p)
                preem_ready_q_p = None
            else:
                CTX_stop_time = -1      #Means this is the process cpu burst end context switch
            if alive_process == 0:
                break

        #Determine if the process arrival time is reached, then add it to the ready queue
        while len(RR_process_list) != 0 and RR_process_list[0].get_arrival_time() == time:
            p = RR_process_list.pop(0)
            ready_Q.append(p)
            #when it's added to the ready queue, set the turnaround start time
            p.set_turnaround_start(time)

            if time < 10000:
                print("time {}ms: Process {} arrived; added to ready queue {}".format(time, p.get_pid(), print_ready_Q(ready_Q)))
        
        #Difference with FCFS, RR will run the process for a time slice
        if RUNNING == 1 and cpu_p.get_expire(time) and cpu_p.get_cpu_burst_stop_time() != time and CTX == 0:
            if ready_Q:
                remaining_time = cpu_p.get_cpu_burst_stop_time() - time
                preemption += 1
                if cpu_p.get_ID() == "CPU-bound":
                    cpu_preemption += 1
                else:
                    io_preemption += 1
                cpu_p.set_remaining_time(remaining_time)

                if time < 10000:
                    print("time {}ms: Time slice expired; preempting process {} with {}ms remaining {}".format(time, cpu_p.get_pid(), remaining_time, print_ready_Q(ready_Q)))
                RUNNING = 0
                context_switch += 0.5
                if cpu_p.get_ID() == "CPU-bound":
                    cpu_context_switch += 0.5
                else:
                    io_context_switch += 0.5
                CTX = 1
                CTX_stop_time = time + half_t_cs
                preem_ready_q_p = cpu_p
                cpu_p = None
            else:
                if time < 10000:
                    print("time {}ms: Time slice expired; no preemption because ready queue is empty {}".format(time, print_ready_Q(ready_Q)))
                cpu_p.set_slice_stop_time(time + t_slice)
        
        #Determine if the CPU is running, and the CPU burst is finished, then change the CPU burst
        if RUNNING == 1 and cpu_p.get_cpu_burst_stop_time() == time and CTX == 0:
            cpu_p.change_cpu_burst()
            cpu_p.set_slice_stop_time(-1)
            RUNNING = 0
            s = ''
            if cpu_p.get_cpu_burst_times() != 1:
                s = 's'
            if time < 10000:
                if cpu_p.get_cpu_burst_times() != 0:
                    print("time {}ms: Process {} completed a CPU burst; {} burst{} to go {}".format(time, cpu_p.get_pid(), cpu_p.get_cpu_burst_times(), s, print_ready_Q(ready_Q)))
            
            #Determine if the process should be terminated, then add it to the finished list, by checking if there's cpu burst times left
            if cpu_p.get_cpu_burst_times() == 0:
                Finished_list.append(cpu_p)
                alive_process -= 1
                print("time {}ms: Process {} terminated {}".format(time, cpu_p.get_pid(), print_ready_Q(ready_Q)))
                #If a process is terminated, then the CPU is free, context switch occurs
                context_switch += 0.5
                if cpu_p.get_ID() == "CPU-bound":
                    cpu_context_switch += 0.5
                else:
                    io_context_switch += 0.5
                CTX = 2
                CTX_stop_time = time + half_t_cs
                cpu_p = None
            #If there's still cpu burst times left, then there must at least have one more I/O burst, so add it to the I/O list
            else:
                #When a process need start a io burst, set io stop time and add it to the io list
                cpu_p.set_io_burst_stop_time(cpu_p.get_io_burst_time(0) + time + half_t_cs)
                io_p = cpu_p
                cpu_p = None
                io_list.append(io_p)
                #sort by io burst stop time to make sure the first process in the io list is the one that will finish the io burst first
                io_list.sort(key=lambda x: x.get_pid())
                io_list.sort(key=lambda x: x.get_io_burst_stop_time())
                if time < 10000:
                    print("time {}ms: Process {} switching out of CPU; blocking on I/O until time {}ms {}".format(time, io_p.get_pid(), io_p.get_io_burst_stop_time(), 
                                                                                                                    print_ready_Q(ready_Q)))
                #when process is switching out of CPU context switch happens, the first half of the context switch is done
                context_switch += 0.5
                if io_p.get_ID() == "CPU-bound":
                    cpu_context_switch += 0.5
                else:
                    io_context_switch += 0.5

                if (ready_Q and ready_Q[0].get_pid() != io_p.get_pid()) or alive_process != 1:
                    CTX = 1
                    CTX_stop_time = time + half_t_cs 
        
        if RUNNING == 0 and (len(ready_Q) != 0 or cpu_p != None) and CTX == 0:
            if CTX_stop_time == -2:
                CTX_stop_time = -4
                RUNNING = 1
                #add another limit of slice stop time
                cpu_p.set_slice_stop_time(t_slice + time)
                
                if cpu_p.get_remaining_time() == -1:
                    #cal cpu burst stop time for comparison later
                    cpu_p.set_cpu_burst_stop_time(cpu_p.get_cpu_burst_time(0) + time)
                    if time < 10000:
                        print("time {}ms: Process {} started using the CPU for {}ms burst {}".format(time, cpu_p.get_pid(), cpu_p.get_cpu_burst_time(0), print_ready_Q(ready_Q)))
                else:
                    #cal cpu burst stop time for comparison later
                    cpu_p.set_cpu_burst_stop_time(cpu_p.get_remaining_time() + time)
                    if time < 10000:
                        print("time {}ms: Process {} started using the CPU for remaining {}ms of {}ms burst {}".format(time, cpu_p.get_pid(), cpu_p.get_remaining_time(), 
                                                                                                                   cpu_p.get_cpu_burst_time(0), print_ready_Q(ready_Q)))
                    cpu_p.set_remaining_time(-1)
            else:
                cpu_p = ready_Q.pop(0)
                CTX = 1
                if io_p != None and io_p.get_pid() == cpu_p.get_pid() and time - io_p.get_io_burst_stop_time() <= half_t_cs:
                    CTX_stop_time = time + half_t_cs - 1
                else:
                    CTX_stop_time = time + half_t_cs

                #when process is switching into CPU context switch happens, the second half of the context switch is done
                context_switch += 0.5
                if cpu_p.get_ID() == "CPU-bound":
                    cpu_context_switch += 0.5
                else:
                    io_context_switch += 0.5
            
        #Determine if a io burst is finished, since the io list is sorted, 
        #the first process in the io list is the one that will finish the io burst first
        while len(io_list) != 0 and io_list[0].get_io_burst_stop_time() == time:
            io_p = io_list.pop(0)
            ready_Q.append(io_p)    
            io_p.change_io_burst()
            if time < 10000:
                print("time {}ms: Process {} completed I/O; added to ready queue {}".format(time, io_p.get_pid(), print_ready_Q(ready_Q)))
          
        time += 1
        
    print("time {}ms: Simulator ended for RR {}\n".format(time, print_ready_Q(ready_Q)))

    #Calculate all data needed for the output file, will use the variable created before algo simulation
    rr_cpu_utilization = math.ceil(((rr_total_cpu_elapsed_time / time) * 100) * 1000) / 1000                                                         
    rr_average_cpu_burst_time = 0                                                                                            
    rr_average_wait_time = 0
    rr_io_wait_time = 0
    rr_cpu_wait_time = 0
    rr_average_turnaround_time = 0
    rr_io_turnaround_time = 0
    rr_cpu_turnaround_time = 0

    #Use for loop to get the data calculated in the simulation
    for p in Finished_list:
        if p.get_ID() == "I/O-bound":
            rr_io_wait_time += p.get_wait_time()
            rr_io_turnaround_time += p.get_turnaround_time()
        else:
            rr_cpu_wait_time += p.get_wait_time()
            rr_cpu_turnaround_time += p.get_turnaround_time()
        rr_average_wait_time += p.get_wait_time()
        rr_total_cpu_burst_times += p.get_cpu_burst_times()

    #Final calculate the data after retriving all the data needed
    rr_average_cpu_burst_time = math.ceil((rr_total_cpu_elapsed_time / rr_total_cpu_burst_times) * 1000 ) / 1000
    rr_cpubound_average_cpu_burst_time = math.ceil((rr_cpubound_cpu_burst_time / cpubound_burst_times) * 1000) / 1000
    rr_iobound_average_cpu_burst_time = math.ceil((rr_iobound_cpu_burst_time / iobound_burst_times) * 1000) / 1000

    rr_total_turnaround_time = rr_io_turnaround_time + rr_cpu_turnaround_time
    rr_iobound_turnaround_time = rr_io_turnaround_time - rr_iobound_io_burst_time
    rr_cpubound_turnaround_time = rr_cpu_turnaround_time - rr_cpubound_io_burst_time

    rr_average_turnaround_time = math.ceil(((rr_total_turnaround_time - rr_total_io_elapsed_time) / rr_total_cpu_burst_times) * 1000) / 1000
    rr_average_cpubound_turnaround_time = math.ceil((rr_cpubound_turnaround_time / cpubound_burst_times) * 1000) / 1000
    rr_average_iobound_turnaround_time = math.ceil((rr_iobound_turnaround_time / iobound_burst_times) * 1000) / 1000

    rr_total_average_context_switch = ((context_switch * t_cs) / rr_total_cpu_burst_times)
    rr_iobound_average_context_switch = ((io_context_switch * t_cs) / iobound_burst_times)
    rr_cpubound_average_context_switch = ((cpu_context_switch * t_cs) / cpubound_burst_times)

    rr_average_wait_time = math.ceil((((rr_total_turnaround_time - rr_total_io_elapsed_time) / rr_total_cpu_burst_times) - (rr_total_cpu_elapsed_time / rr_total_cpu_burst_times) - rr_total_average_context_switch) * 1000) / 1000
    rr_average_cpubound_wait_time = math.ceil(((rr_cpubound_turnaround_time / cpubound_burst_times) - (rr_cpubound_cpu_burst_time / cpubound_burst_times) - rr_cpubound_average_context_switch) * 1000) / 1000
    rr_average_iobound_wait_time = math.ceil(((rr_iobound_turnaround_time / iobound_burst_times) - (rr_iobound_cpu_burst_time / iobound_burst_times) - rr_iobound_average_context_switch) * 1000) / 1000

    rr_context_switch = int(context_switch)
    rr_preemption = preemption
    rr_io_preemption = io_preemption
    rr_cpu_preemption = cpu_preemption

    #Format the output file
    RR_text = (
        "Algorithm RR\n"
        "-- CPU utilization: {:.3f}%\n"
        "-- average CPU burst time: {:.3f} ms ({:.3f} ms/{:.3f} ms)\n"
        "-- average wait time: {:.3f} ms ({:.3f} ms/{:.3f} ms)\n"
        "-- average turnaround time: {:.3f} ms ({:.3f} ms/{:.3f} ms)\n"
        "-- number of context switches: {:.0f} ({:.0f}/{:.0f})\n"
        "-- number of preemptions: {} ({}/{})\n\n"
    ).format(rr_cpu_utilization, 
            rr_average_cpu_burst_time, rr_cpubound_average_cpu_burst_time, rr_iobound_average_cpu_burst_time,
            rr_average_wait_time, rr_average_cpubound_wait_time, rr_average_iobound_wait_time, 
            rr_average_turnaround_time, rr_average_cpubound_turnaround_time, rr_average_iobound_turnaround_time, 
            rr_context_switch, cpu_context_switch, io_context_switch,  
            rr_preemption, rr_cpu_preemption, rr_io_preemption)
    
    #Return the output file, and output to file in project.py
    return RR_text