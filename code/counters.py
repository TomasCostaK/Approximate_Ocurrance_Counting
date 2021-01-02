import sys
import time
import re
class Counter:
    def __init__(self, file_path):
        # Initialize array and declare file_path
        self.file_path = file_path
        self.word_counter_dict = {}
        self.word_counter = 0
    
    def getCount(self):
        return self.word_counter_dict

    # Baseline function, all inherited classes will change this method, this is the method were we split into tokens
    def tokenize(self):
        pass

    def index(self, tokens):
        pass

    def count(self):
        tokens = self.tokenize()
        self.index(tokens)
        return self.word_counter_dict

    def getCounter(self):
        return self.word_counter
class ExactCounter(Counter):
    def tokenize(self):
        print("Exact")
        final_tokens = []
        with open(self.file_path) as file:
            for lines in file:
                tokens = re.sub("[^0-9a-zA-Z]+"," ",lines).lower().split(" ")
                final_tokens.extend(token for token in tokens if len(token)>3)
        return final_tokens

    def index(self, tokens):
        # treatment just for counter
        self.word_counter += len(tokens)

        # treatment if we need each token in a dict
        for token in tokens:
            if token not in self.word_counter_dict.keys():
                self.word_counter_dict[token] = 1
            else:
                self.word_counter_dict[token] += 1
class HalfCounter(Counter):
    def tokenize(self):
        print("Half")

class LogCounter(Counter):
    def tokenize(self):
        print("Log")