class Process(object):
    def __init__(self, arrival_time, ID, pid):
        self.arrival_time = arrival_time
        self.ID = ID
        self.pid = pid
        self.cpu_burst_times = 0
        self.cpu_burst_stop_time = -1
        self.io_burst_times = 0
        self.io_burst_stop_time = -1
        self.turnaround_time = 0
        self.turnaround_time_start = 0
        self.turnaround_time_end = 0
        self.wait_time = 0
        self.wait_time_start = 0
        self.wait_time_end = 0
        self.tau = 1000
    #Below is the concatenation of the string that will be printed out
    def __str__(self) -> str:
        s = ""
        if len(self.cpu_burst_list) != 1:
                s = "s"
        text = "{} process {}: arrival time {}ms; {} CPU burst{}:".format(self.ID, self.pid, self.arrival_time, len(self.cpu_burst_list), s) #for part 1 add \n behind :
        for i in range(len(self.io_burst_list)):
            text += "--> CPU burst {}ms ".format(self.cpu_burst_list[i])
            text += "--> I/O burst {}ms\n".format(self.io_burst_list[i])      #this is for project part 1 output
        text += "--> CPU burst {}ms".format(self.cpu_burst_list[-1])
        return text
    
    #Below is the burst setter for the class
    def set_burst(self, cpu_burst_list, io_burst_list):
        self.cpu_burst_list = cpu_burst_list
        self.cpu_burst_times = len(cpu_burst_list)
        self.io_burst_list = io_burst_list
        self.io_burst_times = len(io_burst_list)
    
    def set_turnaround_start(self, turnaround_time_start):
        self.turnaround_time_start = turnaround_time_start

    def set_turnaround_end(self, turnaround_time_end):
        self.turnaround_time_end = turnaround_time_end
    
    def set_wait_start(self, wait_time_start):
        self.wait_time_start = wait_time_start

    def set_wait_end(self, wait_time_end):
        self.wait_time_end = wait_time_end

    def cal_turnaround_time(self):
        self.turnaround_time = self.turnaround_time_end - self.turnaround_time_start
    
    def cal_wait_time(self):
        self.wait_time += self.wait_time_end - self.wait_time_start
    
    def set_cpu_burst_stop_time(self, cpu_burst_stop_time):
        self.cpu_burst_stop_time = cpu_burst_stop_time
    
    def set_io_burst_stop_time(self, io_burst_stop_time):
        self.io_burst_stop_time = io_burst_stop_time

    def set_tau(self, alpha, burst_time):
        tmp = self.tau
        self.tau = (alpha * burst_time) + ((1-alpha) * tmp)
    
    def change_io_burst(self):
        self.io_burst_list.pop(0)
        self.io_burst_times -= 1
    
    def change_cpu_burst(self):
        self.cpu_burst_list.pop(0)
        self.cpu_burst_times -= 1
    

    #Below are the getters for the class
    def get_cpu_burst(self):
        return self.cpu_burst_list
    
    def get_io_burst(self):
        return self.io_burst_list

    def get_cpu_burst_stop_time(self):
        return self.cpu_burst_stop_time
    
    def get_io_burst_stop_time(self):
        return self.io_burst_stop_time
    
    def get_cpu_burst_time(self, index):
        return self.cpu_burst_list[index]
    
    def get_io_burst_time(self, index):
        return self.io_burst_list[index]
    
    def get_cpu_burst_times(self):
        return self.cpu_burst_times
    
    def get_io_burst_times(self):
        return self.io_burst_times
    
    def get_arrival_time(self):
        return self.arrival_time
    
    def get_sum_cpu_burst(self):
        return sum(self.cpu_burst_list)
    
    def get_sum_io_burst(self):
        return sum(self.io_burst_list)
    
    def get_pid(self):
        return self.pid
    
    def get_tau(self):
        return self.tau
          
    def get_ID(self):
        return self.ID    

    def get_wait_time(self):
        return self.wait_time
    
    def get_turnaround_time(self):
        return self.turnaround_time