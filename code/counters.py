import random
import math
import re
class Counter:
    def __init__(self, file_path):
        # Initialize array and declare file_path
        self.file_path = file_path
        self.tokens = []
        self.word_counter = 0
        self.counter_value = 0

    # Auxiliary function to help call multiple times
    def resetVars(self):
        self.tokens = []
        self.word_counter = 0
        self.counter_value = 0

    def getCount(self):
        return self.word_counter

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

    def count(self):
        self.resetVars()
        self.tokenize()
        self.index()

    def getCounter(self):
        return self.counter_value

    def getWordCounter(self):
        return self.word_counter

    def printCounter(self):
        return f"Counter Value: {self.word_counter}"
class ExactCounter(Counter):
    def index(self):
        # treatment just for counter
        self.word_counter += len(self.tokens)
        self.counter_value += len(self.tokens)

class HalfCounter(Counter):
    def index(self):
        # treatment just for counter
        # other way
        random_array = [random.randint(0,1) for _ in range(len(self.tokens)+1)]
        self.counter_value += sum(random_array)
        self.word_counter += sum(random_array) * 2 # we multiply by 2, since we were predicting only half the events

class LogCounter(Counter):
    def index(self):
        # logarithmic base
        base = math.sqrt(2)
        # treatment just for counter
        for token in self.tokens:
            prob = 1/base**self.counter_value
            if random.random() < prob:
                self.counter_value += 1

        # this formula is provided in the slides as ( a^k–a + 1 ) / ( a –1 )
        k = self.counter_value
        self.word_counter = int((base**k - base + 1 ) / ( base-1 ))
