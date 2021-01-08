import random
import math
import re
from collections import defaultdict 
import math
class Counter:
    def __init__(self, file_path):
        # Initialize array and declare file_path
        self.file_path = file_path
        self.tokens = []
        self.word_dict = defaultdict(lambda:  0)
        self.word_counter = 0
        self.counter_value = 0

    # Auxiliary function to help call multiple times
    def resetVars(self):
        self.tokens = []
        self.word_counter = 0
        self.counter_value = 0
        # we dont reset dict, but print out the values diving by number of trials, since the top10 words should be of all trials
        #self.word_dict = defaultdict(lambda:  0)

    # Baseline function, all inherited classes will change this method, this is the method were we split into tokens
    def tokenize(self):
        final_tokens = []
        with open(self.file_path) as file:
            for lines in file:
                tokens = re.sub("[^0-9a-zA-Z]+"," ",lines).lower().split(" ")
                final_tokens.extend(token for token in tokens if len(token)>3)
        self.tokens.extend(final_tokens)

    def index(self):
        pass

    def addToken(self,token):
        self.word_dict[token] += 1


    def count(self):
        self.resetVars()
        self.tokenize()
        self.index()

    def getCounter(self):
        return self.counter_value
    
    def getCount(self):
        return self.word_counter

    def getTopWords(self, n_trials):
        # returns 10 most frequent
        ten_most_frequent = [(key,value / n_trials) for (key, value) in sorted(
            self.word_dict.items(), key=lambda x: x[1], reverse=True)[:10]]
        return ten_most_frequent

class ExactCounter(Counter):
    def index(self):
        # treatment just for counter
        for token in self.tokens:
            self.addToken(token)
            self.counter_value += 1
        
        # calculate word_value
        self.word_counter += len(self.tokens)
    
    def getDict(self):
        return self.word_dict

class HalfCounter(Counter):
    def index(self):
        # treatment just for counter
        # other way
        random_array = [random.randint(0,1) for _ in range(len(self.tokens))]
        for i in range(len(random_array)):
            if random_array[i] == 1:
                self.addToken(self.tokens[i])
                self.counter_value += 1

        # calculate word_value
        self.word_counter += sum(random_array) * 2
    
    def getTopWords(self,n_trials):
        # returns 10 most frequent
        ten_most_frequent = [(key,value*2/n_trials) for (key, value) in sorted(
            self.word_dict.items(), key=lambda x: x[1], reverse=True)[:10]]
        return ten_most_frequent


class LogCounter(Counter):
    def index(self):
        # logarithmic base
        base = math.sqrt(2)
        # treatment just for counter
        for token in self.tokens:
            prob = 1/base**self.counter_value
            if random.random() < prob:
                self.counter_value += 1
                self.addToken(token)

        # this formula is provided in the slides as ( a^k–a + 1 ) / ( a –1 )
        k = self.counter_value
        self.word_counter = int((base**k - base + 1 ) / ( base-1 ))

    def getTopWords(self, n_trials):
        base = math.sqrt(2)

        # returns 10 most frequent
        ten_most_frequent = [(key, math.ceil((base**(value/n_trials) - base + 1) / (base - 1))) for (key, value) in sorted(
            self.word_dict.items(), key=lambda x: x[1], reverse=True)[:10]]
        return ten_most_frequent

