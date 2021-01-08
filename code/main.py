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
    num_trials = 1
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

    # we calculate exact values to compare afterwards
    counter_exact = ExactCounter(file_path)
    counter_exact.count()
    real_value = counter_exact.getCounter()
    exact_dict = counter_exact.getDict()

    print(f"Executing {num_trials} trials on {type_counter} counter:\n")
    tic = time.time()
    trial_values = []
    for i in range(num_trials):
        counter.count()
        val = counter.getCount()
        trial_values.append(val)

    # evaluate only the last words into a dict
    top_words = counter.getTopWords(num_trials)

    toc = time.time()
    # We use NP to more efficiently calculate averages and std devs
    trial_values = np.array(trial_values)

    # Comparisons
    relative_errors_array = np.absolute(trial_values-real_value) / real_value
    max_re = np.max(relative_errors_array)
    min_re = np.min(relative_errors_array)
    mean_re = np.mean(relative_errors_array)

    # Comparisons
    accuracy_array = np.array(trial_values) / real_value
    mean_acc = np.mean(accuracy_array)

    # Print top words
    print("Ten most frequent words: (average)")
    print("Word \t\t Exact Count \t Est. Count \t Mean absolute error \t Mean relative error")
    print("--------------------------------------------------------------------------------------------")
    for word in top_words:
        print(f"{word[0]} \t\t {exact_dict[word[0]]} \t\t {word[1]} \t\t {abs(word[1]-exact_dict[word[0]]):.1f} \t\t\t {abs(word[1]-exact_dict[word[0]])/ exact_dict[word[0]]*100:.2f}%")

    # Print out measures
    print("\nGlobal counter measures:")
    print(f"Maximum relative error: {max_re*100:.3f}%\nMinimum relative error: {min_re* 100:.3f}% \nMean relative error: {mean_re*100:.3f}% \nMean accuracy ratio: {mean_acc*100:.3f}%\n")
    
    unique, counts = np.unique(trial_values, return_counts=True)
    count_dict = dict(zip(unique, counts))

    # Print out table
    for elem in unique:
        count = count_dict[elem]
        #print(f"counter value: \t{elem},\t {count} times \t- {count/num_trials*100:.2f}%")

    print(f"Calculated in {toc-tic:.2f} seconds")
    # we dont go any further, this is the testing batch
    sys.exit()
