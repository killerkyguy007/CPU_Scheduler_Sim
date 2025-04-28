"""
    Kyran Day
    CS 3502
    Project 2
    This is a class file that holds the MLFQ scheduler. 
    It is a priority based scheduler that uses a time quantum to determine how long a process can run before being preempted.
"""

from scheduler_utils import Process, Metrics, print_results, plot_metrics, input_process

class MLFQ:
    def __init__(self, num_queues=3, time_quantums=[4, 8, 16]):
        self.queues = [[] for _ in range(num_queues)] # Get empty list made
        self.time_quantums = time_quantums
        self.current_time = 0
        self.metrics = Metrics()
        self.time_quantum_used = 0
        
    def add_process(self, process):
        self.queues[0].append(process)  # Add to the highest priority queue
        self.metrics.total_processes += 1
        
    def schedule(self):
        completed_processes = []
        
        while any(queue for queue in self.queues):
            # Find the highest priority non-empty queue
            current_queue = next((i for i, q in enumerate(self.queues) if q), None)
            if current_queue is None:
                self.current_time += 1
                continue
                
            # Get the first process in the current queue
            current_process = self.queues[current_queue][0]
            
            # Record response time if this is first execution
            if current_process.first_execution:
                current_process.response_time = self.current_time - current_process.arrival_time
                current_process.first_execution = False
            
            # Execute for one time unit
            current_process.remaining_time -= 1
            current_process.time_quantum_used += 1
            self.current_time += 1
            self.metrics.cpu_busy_time += 1
            
            # Check if process is completed
            if current_process.remaining_time == 0:
                current_process.completion_time = self.current_time
                current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
                current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
                
                self.metrics.total_waiting_time += current_process.waiting_time
                self.metrics.total_turnaround_time += current_process.turnaround_time
                self.metrics.total_response_time += current_process.response_time
                
                completed_processes.append(current_process)
                self.queues[current_queue].pop(0)
                continue
                
            # Check if time quantum is exhausted
            if current_process.time_quantum_used >= self.time_quantums[current_queue]:
                current_process.time_quantum_used = 0
                # Move to next lower priority queue if not in lowest queue
                if current_queue < len(self.queues) - 1:
                    self.queues[current_queue].pop(0)
                    self.queues[current_queue + 1].append(current_process)
                else:
                    # If in lowest queue, move to back of the queue
                    self.queues[current_queue].pop(0)
                    self.queues[current_queue].append(current_process)
        
        self.metrics.total_time = self.current_time
        return completed_processes, self.metrics

def compare_workloads(workloads):
    print("\nWorkload Comparison Table:")
    print("Workload\tAWT\t\t\tATT\t\t\tCPU Util\tThroughput\tART")
    print("-" * 85)
    
    for i, processes in enumerate(workloads, 1):
        processes_copy = [Process(p.pid, p.arrival_time, p.burst_time) for p in processes]
        scheduler = MLFQ(num_queues=3, time_quantums=[4, 8, 16])
        for process in processes_copy:
            scheduler.add_process(process)
        completed_processes, metrics = scheduler.schedule()
        results = metrics.calculate_metrics()
        print(f"Workload {i}\t{results['Average Waiting Time']:.2f}\t\t{results['Average Turnaround Time']:.2f}\t\t"
              f"{results['CPU Utilization']:.2f}\t\t{results['Throughput']:.2f}\t\t{results['Average Response Time']:.2f}")
