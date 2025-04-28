# CPU Scheduling Algorithms

This project implements and compares two CPU scheduling algorithms:
1. Shortest Remaining Time First (SRTF)
2. Multi-Level Feedback Queue (MLFQ)

## Requirements
- Python 3.x
- matplotlib
- numpy

## Installation
Install the required packages:
```bash
pip install matplotlib numpy
```

## Usage
Run the program:
```bash
python main.py
```

### Menu Options
1. Add new workload
   - Enter number of processes
   - Specify arrival time and burst time for each process

2. Run SRTF scheduler
   - Select a workload to run
   - View detailed results and metrics

3. Run MLFQ scheduler
   - Select a workload to run
   - View detailed results and metrics

4. Compare both schedulers
   - View comparison tables
   - See performance metric plots

5. Exit

## Project Structure
- `main.py`: Main program entry point
- `scheduler_utils.py`: Common utilities and classes
- `srtf_scheduler.py`: SRTF scheduling implementation
- `mlfq_scheduler.py`: MLFQ scheduling implementation

## Author
Kyran Day
CS 3502
Project 2 