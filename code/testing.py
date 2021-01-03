from counters import *
import sys
import time
import numpy as np

def main():
    num_trials = 100
    try:
        num_trials = int(sys.argv[1])
    except Exception:
        print("Unable to parse given number of trials")
        num_trials = 100

    file_path = '../texts/german2.txt' # we can change the file under testing

    print(f"Executing {num_trials} trials on all counters:\n")
    for type_counter in ['Exact','Half', 'Log']:
        counter = None
        # Declare diff type of counters:
        if type_counter == 'Exact':
            counter = ExactCounter(file_path)
        elif type_counter == 'Half':
            counter = HalfCounter(file_path)
        if type_counter == 'Log':
            counter = LogCounter(file_path)

        tic = time.time()
        trial_values = []
        trial_times = []
        for i in range(num_trials):
            counter.count()
            val = counter.getCounter()
            trial_values.append(val)
            toc = time.time()
            trial_times.append(toc-tic)
            tic = toc

        avg_time = np.mean(trial_times)
        avg_count = np.mean(trial_values)        
        
        print(f"{type_counter}:\t {avg_time:.2f} seconds, with {avg_count} counter increments (average)")
    # we dont go any further, this is the testing batch
    sys.exit()

if __name__ == "__main__":
    main()