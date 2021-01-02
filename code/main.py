from counters import *
import sys
import getopt
import random
import time
import os.path

def usage():
    print("Usage: python3 main.py \t(Please provide a type of counter and a file path)\n\t-c,  exact/half/log\t<type of probabilistic counter>\n\t-f,  file_path\t\t<File used for reading>\n\t-t \t\t\t<testing tool option>")

if __name__ == "__main__":
    # initialization of random variables
    type_counter = 'exact'
    testing_flag = False
    file_path = None

    try:
        opts, args = getopt.getopt(sys.argv[1:], "htc:f:", ["help", "output="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err))  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    if "-c" not in [x[0] for x in opts]:
        usage()
        sys.exit(1)
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o == "-t":
            testing_flag = True
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

    if type_counter == 'exact':
        counter = ExactCounter(file_path)
    elif type_counter == 'half':
        counter = HalfCounter(file_path)
    elif type_counter == 'log':
        counter = LogCounter(file_path)
    
    print(counter)
