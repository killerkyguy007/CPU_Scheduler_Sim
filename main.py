"""
    Kyran Day
    CS 3502
    Project 2
    This is a main file that allows the user to run the SRTF and MLFQ schedulers and compare the results.
"""

import sys
import subprocess

def check_dependencies(): # Check for libs
    try:
        import matplotlib
        import numpy
        return True
    except ImportError as e:
        print(f"\nError: Required package not found - {e}")
        print("Please install the required packages using:")
        print("pip install matplotlib numpy")
        return False

def install_dependencies(): # Install libs needed
    print("\nInstalling required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib", "numpy"])
        print("Packages installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("Failed to install packages. Please install them manually.")
        return False

def main():
    # Check dependencies
    if not check_dependencies():
        response = input("\nWould you like to install the required packages now? (y/n): ")
        if response.lower() == 'y':
            if not install_dependencies():
                sys.exit(1)
        else:
            print("Please install the required packages and try again.")
            sys.exit(1)

    # Import after dependency check
    from srtf_scheduler import srtf_scheduling, compare_workloads as compare_srtf
    from mlfq_scheduler import MLFQ, compare_workloads as compare_mlfq
    from scheduler_utils import Process, Metrics, print_results, plot_metrics, input_process

    def compare_schedulers(workloads):
        print("\nSRTF Scheduler Results:")
        compare_srtf(workloads)
        
        print("\nMLFQ Scheduler Results:")
        compare_mlfq(workloads)
        
        # Plot comparison
        srtf_metrics = []
        mlfq_metrics = []
        
        for processes in workloads:
            # SRTF metrics
            processes_copy = [Process(p.pid, p.arrival_time, p.burst_time) for p in processes]
            _, metrics = srtf_scheduling(processes_copy)
            srtf_metrics.append(metrics)
            
            # MLFQ metrics
            processes_copy = [Process(p.pid, p.arrival_time, p.burst_time) for p in processes]
            scheduler = MLFQ(num_queues=3, time_quantums=[4, 8, 16])
            for process in processes_copy:
                scheduler.add_process(process)
            _, metrics = scheduler.schedule()
            mlfq_metrics.append(metrics)
        
        plot_metrics(workloads, srtf_metrics, "SRTF")
        plot_metrics(workloads, mlfq_metrics, "MLFQ")

    def menu():
        workloads = []
        
        while True:
            print("\nMain Menu:")
            print("1. Add new workload")
            print("2. Run SRTF scheduler")
            print("3. Run MLFQ scheduler")
            print("4. Compare both schedulers")
            print("5. Exit")
            
            try:
                choice = input("Enter your choice (1-5): ")
                
                if choice == '1':
                    print("\nEnter process details for new workload:")
                    processes = input_process()
                    workloads.append(processes)
                    print("Workload added successfully!")
                    
                elif choice == '2':
                    if not workloads:
                        print("No workloads available. Please add a workload first.")
                        continue
                        
                    print("\nAvailable workloads:")
                    for i, w in enumerate(workloads, 1):
                        print(f"{i}. Workload {i}")
                    
                    w_choice = int(input("Select workload to run (1-{}): ".format(len(workloads))))
                    if 1 <= w_choice <= len(workloads):
                        processes_copy = [Process(p.pid, p.arrival_time, p.burst_time) for p in workloads[w_choice-1]]
                        completed_processes, metrics = srtf_scheduling(processes_copy)
                        print_results(completed_processes, metrics)
                    else:
                        print("Invalid workload choice!")
                        
                elif choice == '3':
                    if not workloads:
                        print("No workloads available. Please add a workload first.")
                        continue
                        
                    print("\nAvailable workloads:")
                    for i, w in enumerate(workloads, 1):
                        print(f"{i}. Workload {i}")
                    
                    w_choice = int(input("Select workload to run (1-{}): ".format(len(workloads))))
                    if 1 <= w_choice <= len(workloads):
                        processes_copy = [Process(p.pid, p.arrival_time, p.burst_time) for p in workloads[w_choice-1]]
                        scheduler = MLFQ(num_queues=3, time_quantums=[4, 8, 16])
                        for process in processes_copy:
                            scheduler.add_process(process)
                        completed_processes, metrics = scheduler.schedule()
                        print_results(completed_processes, metrics)
                    else:
                        print("Invalid workload choice!")
                        
                elif choice == '4':
                    if len(workloads) < 2:
                        print("Need at least 2 workloads for comparison!")
                        continue
                    compare_schedulers(workloads)
                    
                elif choice == '5': 
                    print("Exiting...")
                    break
                    
                else:
                    print("Invalid choice! Please try again.")
            #EndTry
            except ValueError:
                print("Please enter a valid number.")
            except KeyboardInterrupt:
                print("\nProgram terminated by user.")
                break
            except Exception as e:
                print(f"An error occurred: {e}")

    print("\nWelcome to the CPU Scheduling Simulator!")
    print("------------------------------------")
    menu()

if __name__ == "__main__":
    main() 