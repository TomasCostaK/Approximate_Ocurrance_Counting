import random
import re
class Counter:
    def __init__(self, file_path):
        # Initialize array and declare file_path
        self.file_path = file_path
        self.word_counter = 0
    
    def getCount(self):
        return self.word_counter

    # Baseline function, all inherited classes will change this method, this is the method were we split into tokens
    def tokenize(self):
        final_tokens = []
        with open(self.file_path) as file:
            for lines in file:
                tokens = re.sub("[^0-9a-zA-Z]+"," ",lines).lower().split(" ")
                final_tokens.extend(token for token in tokens if len(token)>3)
        return final_tokens

    def index(self, tokens):
        pass

    def count(self):
        tokens = self.tokenize()
        self.index(tokens)

    def getCounter(self):
        return f"Counter: {self.word_counter}"
class ExactCounter(Counter):
    def index(self, tokens):
        # treatment just for counter
        self.word_counter += len(tokens)
        
class HalfCounter(Counter):
    def index(self, tokens):
        # treatment just for counter
        # other way
        random_array = [random.randint(0,1) for _ in range(len(tokens)+1)]
        self.word_counter += sum(random_array) * 2 # we multiply by 2, since we were predicting only half the events

class LogCounter(Counter):
    def index(self):
        # treatment just for counter
        random_array = [random.randint(0,1) for _ in range(len(tokens)+1)]
        self.word_counter += sum(random_array) * 2