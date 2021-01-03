from counters import *
import sys
import getopt
import random
import time
import os.path
import numpy as np

def usage():
    print("Usage: python3 main.py \t(Please provide a type of counter and a file path)\n\t-c,  exact/half/log\t<type of probabilistic counter>\n\t-f,  file_path\t\t<File used for reading>\n\t-t,  int\t\t<number of trials>")

if __name__ == "__main__":
    # initialization of random variables
    type_counter = 'exact'
    num_trials = None
    file_path = None

    try:
        opts, args = getopt.getopt(sys.argv[1:], "ht:c:f:", ["help", "output="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err))  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    temp_opts = [x[0] for x in opts]
    if "-c" not in temp_opts or "-f" not in temp_opts:
        usage()
        sys.exit(1)
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o == "-t":
            try:
                num_trials = int(a)
            except Exception:
                print("Provide and Integer for number of trials")
                usage()
                sys.exit()
        elif o == "-f":
            if os.path.isfile(a):
                file_path = a
            else:
                print ("File does not exist")
                usage()
                sys.exit()

        elif o == "-c":
            if a in ['exact','half','log']:
                type_counter = a
            else: 
                usage()
                sys.exit()

    # The individual analysis for each text, given that -c and -f is provided
    if type_counter == 'exact':
        counter = ExactCounter(file_path)
    elif type_counter == 'half':
        counter = HalfCounter(file_path)
    elif type_counter == 'log':
        counter = LogCounter(file_path)

    if num_trials != None:
        # we calculate exact values to compare afterwards
        counter_exact = ExactCounter(file_path)
        counter_exact.count()
        real_value = counter_exact.getCounter()


        print(f"Executing {num_trials} trials on {type_counter} counter:\n")
        tic = time.time()
        trial_values = []
        for i in range(num_trials):
            counter.count()
            val = counter.getWordCounter()
            trial_values.append(val)

        toc = time.time()
        # We use NP to more efficiently calculate averages and std devs
        trial_values = np.array(trial_values)
        
        # Measures
        mean = np.mean(trial_values)
        low = np.min(trial_values)
        high = np.max(trial_values)
        mean_abs_dev = np.mean(np.absolute(trial_values - np.mean(trial_values)))
        std_dev = np.std(trial_values)
        variance = np.var(trial_values)

        # Comparisons
        relative_errors_array = np.absolute(trial_values-real_value)
        maxre = np.max(relative_errors_array)
        minre = np.min(relative_errors_array)

        # Print out measures
        print(f"Smallest counter value: {low} \nHighest counter value: {high}\nMaximum relative error: {maxre:.3f}\nMinimum relative error: {minre:.3f} \nMean counter value: {mean:.3f} \nMean absolute deviation: {mean_abs_dev:.3f} \nStandard deviation: {std_dev:.3f} \nVariance: {variance:.3f}\n")
        
        unique, counts = np.unique(trial_values, return_counts=True)
        count_dict = dict(zip(unique, counts))

        # Print out table
        for elem in unique:
            count = count_dict[elem]
            print(f"counter value: \t{elem},\t {count} times \t- {count/num_trials*100:.1f}%")

        print(f"Calculated in {toc-tic:.2f} seconds")
        # we dont go any further, this is the testing batch
        sys.exit()

    # Counting needs to happen before
    counter.count()
    print(counter.printCounter())
