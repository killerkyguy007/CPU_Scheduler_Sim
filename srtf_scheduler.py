"""
    Kyran Day
    CS 3502
    Project 2
    This file implements the Shortest Remaining Time First (SRTF) scheduler. 
    It is a preemptive scheduler that always runs the process with the shortest remaining time.
"""

from scheduler_utils import Process, Metrics

def srtf_scheduling(processes):
    n = len(processes)
    current_time = 0
    completed = 0
    metrics = Metrics()
    metrics.total_processes = n
    
    # Sort processes by arrival time
    processes.sort(key=lambda x: x.arrival_time)
    
    while completed != n:
        # Find processes that have arrived and have remaining time
        ready_processes = [p for p in processes if p.arrival_time <= current_time and p.remaining_time > 0]
        
        if not ready_processes:
            current_time += 1
            continue
            
        # Find process with shortest remaining time
        current_process = min(ready_processes, key=lambda x: x.remaining_time)
        
        # Record response time if this is first execution
        if current_process.first_execution:
            current_process.response_time = current_time - current_process.arrival_time
            current_process.first_execution = False
        
        # Execute for 1 time unit
        current_process.remaining_time -= 1
        current_time += 1
        metrics.cpu_busy_time += 1
        
        # If process is completed
        if current_process.remaining_time == 0:
            completed += 1
            current_process.completion_time = current_time
            current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
            current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
            
            metrics.total_waiting_time += current_process.waiting_time
            metrics.total_turnaround_time += current_process.turnaround_time
            metrics.total_response_time += current_process.response_time
    
    metrics.total_time = current_time
    return processes, metrics

def compare_workloads(workloads):
    print("\nWorkload Comparison Table:")
    print("Workload\tAWT\t\t\tATT\t\t\tCPU Util\tThroughput\tART")
    print("-" * 85)
    
    for i, processes in enumerate(workloads, 1):
        processes_copy = [Process(p.pid, p.arrival_time, p.burst_time) for p in processes]
        completed_processes, metrics = srtf_scheduling(processes_copy)
        results = metrics.calculate_metrics()
        print(f"Workload {i}\t{results['Average Waiting Time']:.2f}\t\t{results['Average Turnaround Time']:.2f}\t\t"
              f"{results['CPU Utilization']:.2f}\t\t{results['Throughput']:.2f}\t\t{results['Average Response Time']:.2f}")
