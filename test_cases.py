import random

def generate_test_case(num_processes, max_arrival=100, max_burst=20):
    """Generate a test case with random processes."""
    processes = []
    for i in range(num_processes):
        arrival_time = random.randint(0, max_arrival)
        burst_time = random.randint(1, max_burst)
        processes.append(f"{i+1},{arrival_time},{burst_time}")
    return processes

def save_test_case(processes, filename):
    """Save test case to a file."""
    with open(filename, 'w') as f:
        f.write("PID,Arrival Time,Burst Time\n")
        for process in processes:
            f.write(f"{process}\n")

def main():
    # Generate test cases with different numbers of processes
    test_cases = {
        "test_case_10.txt": 10,
        "test_case_20.txt": 20,
        "test_case_30.txt": 30,
        "test_case_40.txt": 40,
        "test_case_50.txt": 50
    }
    
    print("Generating test cases...")
    for filename, num_processes in test_cases.items():
        processes = generate_test_case(num_processes)
        save_test_case(processes, filename)
        print(f"Generated {filename} with {num_processes} processes")
    
    print("\nTest cases have been generated and saved to files.")
    print("You can use these files with your scheduler implementations.")
    print("\nTo run the schedulers with these test cases:")
    print("1. Make sure Python is properly installed")
    print("2. Install required packages: pip install matplotlib numpy")
    print("3. Run main.py and use the test case files")

if __name__ == "__main__":
    main() 