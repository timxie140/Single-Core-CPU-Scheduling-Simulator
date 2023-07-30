from copy import deepcopy
from process import Process

def print_ready_Q(ready_Q):
    if len(ready_Q) != 0:
        text = "[Q"
        for p in ready_Q:
            text += " {}".format(p.pid)
        text += "]"
    else:
        text = "[Q <empty>]"
    return text

def FCFS (process_list, t_cs):
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

    Finished_list = []

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

    print("time {}ms: Simulator started for FCFS {}".format(time, print_ready_Q(ready_Q)))

    while alive_process != 0:
        if len(FCFS_process_list) != 0 and FCFS_process_list[0].get_arrival_time() == time:
            p = FCFS_process_list.pop(0)
            ready_Q.append(p)
            p.set_turnaround_start(time)
            p.set_wait_start(time)
            if time < 10000:
                print("time {}ms: Process {} arrived; added to ready queue {}".format(time, p.get_pid(), print_ready_Q(ready_Q)))
            
        if RUNNING == 1 and cpu_p.get_cpu_burst_stop_time() == time:
            cpu_p.change_cpu_burst()
            RUNNING = 0
            if time < 10000:
                print("time {}ms: Process {} completed a CPU burst; {} bursts to go {}".format(time, cpu_p.get_pid(), cpu_p.get_cpu_burst_times(), print_ready_Q(ready_Q)))
            if cpu_p.get_cpu_burst_times() == 0:
                Finished_list.append(cpu_p)
                alive_process -= 1
                print("time {}ms: Process {} terminated {}".format(time, cpu_p.get_pid(), print_ready_Q(ready_Q)))
                context_switch += 0.5
                if cpu_p.get_ID() == "CPU-bound":
                    cpu_context_switch += 0.5
                else:
                    io_context_switch += 0.5
                time += half_t_cs
                cpu_p.set_turnaround_end(time)
                cpu_p.cal_turnaround_time()
                cpu_p = None
            else:
                cpu_p.set_io_burst_stop_time(cpu_p.get_io_burst_time(0) + time + half_t_cs)
                io_p = cpu_p
                cpu_p = None
                io_list.append(io_p)
                io_list.sort(key=lambda x: x.get_io_burst_stop_time())
                if time < 10000:
                    print("time {}ms: Process {} switching out of CPU; will block on I/O until time {}ms {}".format(time, io_p.get_pid(), io_p.get_io_burst_stop_time(), print_ready_Q(ready_Q)))
                context_switch += 0.5
                if io_p.get_ID() == "CPU-bound":
                    cpu_context_switch += 0.5
                else:
                    io_context_switch += 0.5
                if ready_Q and ready_Q[0].get_pid() != io_p.get_pid():
                    time += half_t_cs
                # io_p.set_turnaround_end(time)
                # io_p.cal_turnaround_time()
        
        if len(io_list) != 0 and io_list[0].get_io_burst_stop_time() == time:
            io_p = io_list.pop(0)
            ready_Q.append(io_p)    
            io_p.change_io_burst()
            if time < 10000:
                print("time {}ms: Process {} completed I/O; added to ready queue {}".format(time, io_p.get_pid(), print_ready_Q(ready_Q)))
            io_p.set_wait_start(time)
            # io_p.set_turnaround_start(time)
        
        if RUNNING == 0 and len(ready_Q) != 0:
            cpu_p = ready_Q.pop(0)
            cpu_p.set_wait_end(time)
            cpu_p.cal_wait_time()
            time += half_t_cs
            context_switch += 0.5
            if cpu_p.get_ID() == "CPU-bound":
                cpu_context_switch += 0.5
            else:
                io_context_switch += 0.5
            RUNNING = 1
            cpu_p.set_cpu_burst_stop_time(cpu_p.get_cpu_burst_time(0) + time)
            if time < 10000:
                print("time {}ms: Process {} started using the CPU for {}ms burst {}".format(time, cpu_p.get_pid(), cpu_p.get_cpu_burst_time(0), print_ready_Q(ready_Q)))
        if alive_process != 0:    
            time += 1
    print("time {}ms: Simulator ended for FCFS".format(time))

    fcfs_cpu_utilization = (fcfs_total_cpu_elapsed_time / time) * 100                                                               #DONE
    fcfs_average_cpu_burst_time = 0                                                                                                 #DONE
    fcfs_average_wait_time = 0
    fcfs_io_wait_time = 0
    fcfs_cpu_wait_time = 0
    fcfs_average_turnaround_time = 0
    fcfs_io_turnaround_time = 0
    fcfs_cpu_turnaround_time = 0

    for p in Finished_list:
        if p.get_ID() == "I/O-bound":
            fcfs_io_wait_time += p.get_wait_time()
            fcfs_io_turnaround_time += p.get_turnaround_time()
        else:
            fcfs_cpu_wait_time += p.get_wait_time()
            fcfs_cpu_turnaround_time += p.get_turnaround_time()
        fcfs_average_wait_time += p.get_wait_time()
        fcfs_total_cpu_burst_times += p.get_cpu_burst_times()

    fcfs_average_cpu_burst_time = fcfs_total_cpu_elapsed_time / fcfs_total_cpu_burst_times                                     #DONE    
    fcfs_average_wait_time /= fcfs_total_cpu_burst_times
    fcfs_average_turnaround_time = ((fcfs_io_turnaround_time + fcfs_cpu_turnaround_time) - fcfs_total_io_elapsed_time) / fcfs_total_cpu_burst_times
    fcfs_context_switch = int(context_switch)
    fcfs_preemption = 0

    FCFS_text = (
        "Algorithm FCFS\n"
        "-- CPU utilization: {:.3f}%\n"
        "-- average CPU burst time: {:.3f} ms ({:.3f} ms/{:.3f} ms)\n"
        "-- average wait time: {:.3f} ms ({:.3f} ms/{:.3f} ms)\n"
        "-- average turnaround time: {:.3f} ms ({:.3f} ms/{:.3f} ms)\n"
        "-- number of context switches: {:.0f} ({:.0f}/{:.0f})\n"
        "-- number of preemptions: {} ({}/{})\n"
    ).format(fcfs_cpu_utilization, 
            fcfs_average_cpu_burst_time, fcfs_cpubound_cpu_burst_time / cpubound_burst_times, fcfs_iobound_cpu_burst_time / iobound_burst_times,
            fcfs_average_wait_time, fcfs_cpu_wait_time / cpubound_burst_times, fcfs_io_wait_time / iobound_burst_times, 
            fcfs_average_turnaround_time, (fcfs_cpu_turnaround_time - fcfs_cpubound_io_burst_time) / cpubound_burst_times, (fcfs_io_turnaround_time - fcfs_iobound_io_burst_time) / iobound_burst_times, 
            fcfs_context_switch, io_context_switch, cpu_context_switch, 
            fcfs_preemption, fcfs_preemption, fcfs_preemption)
    
    return FCFS_text