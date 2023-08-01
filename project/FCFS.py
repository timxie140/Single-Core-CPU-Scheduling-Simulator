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

#function of the full FCFS algorithm
def FCFS (process_list, t_cs):
    #Below is the variables used in the algo
    time = 0
    half_t_cs = t_cs // 2
    ready_Q = []
    RUNNING = 0
    cpu_p = None
    io_p = None
    io_list = []
    FCFS_process_list = deepcopy(process_list)
    FCFS_process_list.sort(key=lambda x: x.get_arrival_time())
    alive_process = len(process_list)

    CTX = 0
    CTX_stop_time = -1

    #Below is the variables used to calculate the data
    fcfs_total_cpu_burst_times = 0
    fcfs_total_cpu_elapsed_time = 0
    fcfs_total_io_elapsed_time = 0

    context_switch = 0
    io_context_switch = 0
    cpu_context_switch = 0
    
    iobound_burst_times = 0
    cpubound_burst_times = 0

    fcfs_iobound_cpu_burst_time = 0
    fcfs_cpubound_cpu_burst_time = 0
    fcfs_iobound_io_burst_time = 0
    fcfs_cpubound_io_burst_time = 0

    #Below is the list of finished process
    Finished_list = []

    #Using for loop to prerecord the data that will not be available after the FCFS runs
    for p in FCFS_process_list:
        fcfs_total_cpu_elapsed_time += p.get_sum_cpu_burst()
        fcfs_total_cpu_burst_times += p.get_cpu_burst_times()
        fcfs_total_io_elapsed_time += p.get_sum_io_burst()
        if p.get_ID() == "I/O-bound":
            iobound_burst_times += p.get_cpu_burst_times()
            fcfs_iobound_cpu_burst_time += p.get_sum_cpu_burst()
            fcfs_iobound_io_burst_time += p.get_sum_io_burst()
        else:
            cpubound_burst_times += p.get_cpu_burst_times()
            fcfs_cpubound_cpu_burst_time += p.get_sum_cpu_burst()
            fcfs_cpubound_io_burst_time += p.get_sum_io_burst()

    #Starting the FCFS
    print("time {}ms: Simulator started for FCFS {}".format(time, print_ready_Q(ready_Q)))

    #FCFS algo runs here
    while alive_process != 0 or CTX != 0:
        if CTX_stop_time == time:
            if CTX == 2:        #If the process is terminated
                #Set the turnaround end time and calculate the turnaround time
                Finished_list[-1].set_turnaround_end(time)
                Finished_list[-1].cal_turnaround_time()
            CTX = 0
            if RUNNING == 0 and cpu_p != None:
                CTX_stop_time = -2      #Means this is the process cpu burst start context switch
            else:
                CTX_stop_time = -1      #Means this is the process cpu burst end context switch
            if alive_process == 0:
                break
                
        #Determine if the process arrival time is reached, then add it to the ready queue
        while len(FCFS_process_list) != 0 and FCFS_process_list[0].get_arrival_time() == time:
            p = FCFS_process_list.pop(0)
            ready_Q.append(p)
            #when it's added to the ready queue, set the turnaround start time
            p.set_turnaround_start(time)
            if time < 10000:
                print("time {}ms: Process {} arrived; added to ready queue {}".format(time, p.get_pid(), print_ready_Q(ready_Q)))
        
        #Determine if the CPU is running, and the CPU burst is finished, then change the CPU burst
        if RUNNING == 1 and cpu_p.get_cpu_burst_stop_time() == time and CTX == 0:
            cpu_p.change_cpu_burst()
            RUNNING = 0
            s = ''
            if cpu_p.get_cpu_burst_times() != 1:
                s = 's'
            if time < 10000 and cpu_p.get_cpu_burst_times() != 0:
                if cpu_p.get_cpu_burst_times() != 0:
                    print("time {}ms: Process {} completed a CPU burst; {} burst{} to go {}".format(time, cpu_p.get_pid(), cpu_p.get_cpu_burst_times(), s, print_ready_Q(ready_Q)))
            
            #Determine if the process should be terminated, then add it to the finished list, by checking if there's cpu burst times left
            if cpu_p.get_cpu_burst_times() == 0:
                Finished_list.append(cpu_p)
                print("time {}ms: Process {} terminated {}".format(time, cpu_p.get_pid(), print_ready_Q(ready_Q)))

                alive_process -= 1
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
                    print("time {}ms: Process {} switching out of CPU; blocking on I/O until time {}ms {}".format(time, io_p.get_pid(), io_p.get_io_burst_stop_time(), print_ready_Q(ready_Q)))

                #when process is switching out of CPU context switch happens, the first half of the context switch is done
                context_switch += 0.5
                if io_p.get_ID() == "CPU-bound":
                    cpu_context_switch += 0.5
                else:
                    io_context_switch += 0.5
                if ready_Q and ready_Q[0].get_pid() != io_p.get_pid():
                    CTX = 1
                    CTX_stop_time = time + half_t_cs               

        #Determine if the CPU is free, and there's process in the ready queue, then start the process
        if RUNNING == 0 and (len(ready_Q) != 0 or cpu_p != None) and CTX == 0:
            if CTX_stop_time == -2:
                CTX_stop_time = -4
                #when the process is taking out of the ready queue, set the wait end time and calculate the wait time
                RUNNING = 1
                #cal cpu burst stop time for comparison later
                cpu_p.set_cpu_burst_stop_time(cpu_p.get_cpu_burst_time(0) + time)
                if time < 10000:
                    print("time {}ms: Process {} started using the CPU for {}ms burst {}".format(time, cpu_p.get_pid(), cpu_p.get_cpu_burst_time(0), print_ready_Q(ready_Q)))
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
    print("time {}ms: Simulator ended for FCFS {}\n".format(time, print_ready_Q(ready_Q)))

    #Calculate all data needed for the output file, will use the variable created before algo simulation
    fcfs_cpu_utilization = math.ceil(((fcfs_total_cpu_elapsed_time / time) * 100) * 1000) / 1000                                                         
    fcfs_average_cpu_burst_time = 0                                                                                            
    fcfs_average_wait_time = 0
    fcfs_io_wait_time = 0
    fcfs_cpu_wait_time = 0
    fcfs_average_turnaround_time = 0
    fcfs_io_turnaround_time = 0
    fcfs_cpu_turnaround_time = 0

    #Use for loop to get the data calculated in the simulation
    for p in Finished_list:
        if p.get_ID() == "I/O-bound":
            fcfs_io_wait_time += p.get_wait_time()
            fcfs_io_turnaround_time += p.get_turnaround_time()
        else:
            fcfs_cpu_wait_time += p.get_wait_time()
            fcfs_cpu_turnaround_time += p.get_turnaround_time()
        fcfs_average_wait_time += p.get_wait_time()
        fcfs_total_cpu_burst_times += p.get_cpu_burst_times()

    #Final calculate the data after retriving all the data needed
    fcfs_average_cpu_burst_time = math.ceil((fcfs_total_cpu_elapsed_time / fcfs_total_cpu_burst_times) * 1000 ) / 1000
    fcfs_cpubound_average_cpu_burst_time = math.ceil((fcfs_cpubound_cpu_burst_time / cpubound_burst_times) * 1000) / 1000
    fcfs_iobound_average_cpu_burst_time = math.ceil((fcfs_iobound_cpu_burst_time / iobound_burst_times) * 1000) / 1000

    fcfs_total_turnaround_time = fcfs_io_turnaround_time + fcfs_cpu_turnaround_time
    fcfs_iobound_turnaround_time = fcfs_io_turnaround_time - fcfs_iobound_io_burst_time
    fcfs_cpubound_turnaround_time = fcfs_cpu_turnaround_time - fcfs_cpubound_io_burst_time

    fcfs_average_turnaround_time = math.ceil(((fcfs_total_turnaround_time - fcfs_total_io_elapsed_time) / fcfs_total_cpu_burst_times) * 1000) / 1000
    fcfs_average_cpubound_turnaround_time = math.ceil((fcfs_cpubound_turnaround_time / cpubound_burst_times) * 1000) / 1000
    fcfs_average_iobound_turnaround_time = math.ceil((fcfs_iobound_turnaround_time / iobound_burst_times) * 1000) / 1000

    fcfs_average_wait_time = math.ceil((((fcfs_total_turnaround_time - fcfs_total_io_elapsed_time) / fcfs_total_cpu_burst_times) - (fcfs_total_cpu_elapsed_time / fcfs_total_cpu_burst_times) - t_cs) * 1000) / 1000
    fcfs_average_cpubound_wait_time = math.ceil(((fcfs_cpubound_turnaround_time / cpubound_burst_times) - (fcfs_cpubound_cpu_burst_time / cpubound_burst_times) - t_cs) * 1000) / 1000
    fcfs_average_iobound_wait_time = math.ceil(((fcfs_iobound_turnaround_time / iobound_burst_times) - (fcfs_iobound_cpu_burst_time / iobound_burst_times) - t_cs) * 1000) / 1000

    fcfs_context_switch = int(context_switch)
    fcfs_preemption = 0

    #Format the output file
    FCFS_text = (
        "Algorithm FCFS\n"
        "-- CPU utilization: {:.3f}%\n"
        "-- average CPU burst time: {:.3f} ms ({:.3f} ms/{:.3f} ms)\n"
        "-- average wait time: {:.3f} ms ({:.3f} ms/{:.3f} ms)\n"
        "-- average turnaround time: {:.3f} ms ({:.3f} ms/{:.3f} ms)\n"
        "-- number of context switches: {:.0f} ({:.0f}/{:.0f})\n"
        "-- number of preemptions: {} ({}/{})\n\n"
    ).format(fcfs_cpu_utilization, 
            fcfs_average_cpu_burst_time, fcfs_cpubound_average_cpu_burst_time, fcfs_iobound_average_cpu_burst_time,
            fcfs_average_wait_time, fcfs_average_cpubound_wait_time, fcfs_average_iobound_wait_time, 
            fcfs_average_turnaround_time, fcfs_average_cpubound_turnaround_time, fcfs_average_iobound_turnaround_time, 
            fcfs_context_switch, cpu_context_switch, io_context_switch,  
            fcfs_preemption, fcfs_preemption, fcfs_preemption)
    
    #Return the output file, and output to file in project.py
    return FCFS_text