import sys
import time
class Counter:
    def __init__(self, file_path):
        # Initialize array and declare file_path
        self.file_path = file_path
    
    def getCount(self):
        return self.file_path

    __getCount = getCount

class ExactCounter(Counter):
    def getCount(self):
        return self.file_path

class HalfCounter(Counter):
    def getCount(self):
        return self.file_path

class LogCounter(Counter):
    def getCount(self):
        return self.file_path