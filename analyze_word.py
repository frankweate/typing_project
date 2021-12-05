import time
import math
import numpy as np
class Word():
    
    def __init__(self):
        self.previous_time = time.time()
        self.word_count = 0
        self.average = 0
        self.words = {}
        previous_time = 0
    def update_word_time(self,word):
        current_time = time.time()
        new_time = (current_time - self.previous_time) / len(word)
        self.average = (self.average * self.word_count + new_time) / (self.word_count + 1)
        self.word_count +=1
        if word in self.words:
            word_time, count = self.words[word]
            word_time = (word_time*count + new_time)/(count+1)
            self.words[word] = [word_time,count+1]
        else:
            self.words[word] = [new_time,1]
        #print(new_time)
        self.previous_time = current_time
        return new_time
    def get_data(self):
        data = [(k,v) for k,v in self.words.items()]
        data.sort(key=self.sort_data, reverse=True)
        return data ,self.average
        
    def sort_data(self,elem):
        return float(elem[1][0])
