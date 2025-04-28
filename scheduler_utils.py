"""
    Kyran Day
    CS 3502
    Project 2
    This is a class file that holds the Process and Metrics classes.
    The Process class is used to create a process with a pid, arrival time, burst time, remaining time, completion time, waiting time, turnaround time, and response time.
    The Metrics class is used to calculate the metrics for the processes.
"""

import matplotlib.pyplot as plt
import numpy as np

class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = -1  # -1 indicates not yet responded
        self.first_execution = True
        self.time_quantum_used = 0
class Metrics:
    def __init__(self):
        self.total_waiting_time = 0
        self.total_turnaround_time = 0
        self.total_response_time = 0
        self.cpu_busy_time = 0
        self.total_processes = 0
        self.total_time = 0

    def calculate_metrics(self): # Calculate the metrics
        return {
            "Average Waiting Time": self.total_waiting_time / self.total_processes,
            "Average Turnaround Time": self.total_turnaround_time / self.total_processes,
            "CPU Utilization": (self.cpu_busy_time / self.total_time) * 100 if self.total_time > 0 else 0,
            "Throughput": self.total_processes / self.total_time if self.total_time > 0 else 0,
            "Average Response Time": self.total_response_time / self.total_processes if self.total_processes > 0 else 0
        }

def print_results(processes, metrics): # Print the results
    print("\nProcess\t\tArrival Time\tBurst Time\tCompletion Time\tWaiting Time\tTurnaround Time\tResponse Time")
    for p in processes:
        print(f"{p.pid}\t\t\t{p.arrival_time}\t\t\t\t{p.burst_time}\t\t\t{p.completion_time}\t\t\t\t{p.waiting_time}"
              f"\t\t\t\t{p.turnaround_time}\t\t\t\t{p.response_time}")
    
    results = metrics.calculate_metrics()
    print("\nPerformance Metrics:")
    print(f"Average Waiting Time: {results['Average Waiting Time']:.2f}")
    print(f"Average Turnaround Time: {results['Average Turnaround Time']:.2f}")
    print(f"CPU Utilization: {results['CPU Utilization']:.2f}%")
    print(f"Throughput: {results['Throughput']:.2f} processes/second")
    print(f"Average Response Time: {results['Average Response Time']:.2f}")

def plot_metrics(workloads, metrics_list, scheduler_name): # Plot the metrics for each workload
    metrics = ['Average Waiting Time', 'Average Turnaround Time', 'CPU Utilization', 'Throughput', 'Average Response Time']
    x = np.arange(len(workloads))
    width = 0.15
    
    fig, ax = plt.subplots(figsize=(12, 6)) # Create a figure and axis
    
    for i, metric in enumerate(metrics): # Plot the metrics for each workload
        values = [m.calculate_metrics()[metric] for m in metrics_list]
        ax.bar(x + i*width, values, width, label=metric)
    
    ax.set_xlabel('Workloads') # Set the x-axis label
    ax.set_ylabel('Value') # Set the y-axis label
    ax.set_title(f'Performance Metrics Comparison - {scheduler_name}') # Set the title
    ax.set_xticks(x + width*2) # Set the x-ticks
    ax.set_xticklabels([f'Workload {i+1}' for i in range(len(workloads))]) # Set the x-tick labels
    ax.legend() # Show the legend
    
    plt.tight_layout() # Adjust layout
    plt.show() # Show the plot

def input_process(): # Creata a list of processes
    processes = []
    n = int(input("Enter number of processes: "))
    for i in range(n):
        print(f"\nProcess {i+1}:")
        arrival_time = int(input("Enter arrival time: "))
        burst_time = int(input("Enter burst time: "))
        processes.append(Process(i+1, arrival_time, burst_time))
    return processes 