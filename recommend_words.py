import numpy
import csv
import os
import random
import time
import math
# the class that handles the recommendation logic for words.
class RecommendWords:
    hash_table = {}
    word_ranks = []
    rank_lookup = {}
    rank_total = 0
    def __init__(self):
        #create a hash table of all our words so we can retrieve them from the file 
        #in constant time
        
        rankfile = open("csv_files/word_rank.csv","r")
        rankfile_reader = csv.reader(rankfile)
        
        for row in rankfile_reader:
            self.rank_total += int(row[1])
            self.word_ranks.append((row[0],self.rank_total))
            self.rank_lookup[row[0]] = int(row[1])
        rankfile.close()

        wordfile = open("csv_files/top_words_freq.csv","r") 
        wordfile_reader = csv.reader(wordfile)
        graphfile = open("csv_files/graph.csv")
        row = graphfile.readline()
        offset = 0
        while row:
            wordrow = next(wordfile_reader)
            self.hash_table[wordrow[0]] = offset 
            offset = graphfile.tell()
            row = graphfile.readline()
            
              
        wordfile.close()
        graphfile.close()
        
    def convert_string_to_list(self,string):
        result = string.strip(')][(').split('), (')
        list_tuple = []
        for i in result:
            vals = i.strip('\'').split('\', ')
            list_tuple.append((vals[0],float(vals[1])))
        return list_tuple

    def get_word_edges(self,word):
        file = open("csv_files/graph.csv")
        offset = self.hash_table[word]
        graphfile = open("csv_files/graph.csv")
        reader = csv.reader(graphfile)
        graphfile.seek(offset,0)
        edge_string = next(reader)[1]
        return self.convert_string_to_list(edge_string)
    
    def get_paragraph(self,word_metrics,alpha,number_of_words):
        #contains a list with item [wordname, average_word_time]
        paragraph = []
        #effective words per minute 
        ewpm = 0
        if len(word_metrics) == 0:
            for _ in range(0,number_of_words):
                paragraph.append(self.get_weighted_random_word())
        else:
            word_time_list, average = word_metrics
            slow_word_list,ewpm = self.get_inefficency_list(word_time_list,average)
            #worst_percentage is the length of the list that we will iterate over
            # 
            worst_percentage = min(math.floor(alpha * number_of_words/ 2), len(slow_word_list))
            for i in range(0,worst_percentage):
                #for these underperforming nodes we want to get 2 similar nodes from the wordlist and add them to the next paragraph
                edges = self.get_word_edges(slow_word_list[i][0])
                paragraph.append(self.get_random_edge(edges))
                paragraph.append(self.get_random_edge(edges))
            
            random_words_to_add_to_paragraph = number_of_words - worst_percentage*2
            for _ in range(0,random_words_to_add_to_paragraph):
                paragraph.append(self.get_weighted_random_word())
                
        random.shuffle(paragraph)
        return paragraph , ewpm

    def get_random_edge(self,edges):
        rand_weight = random.random()
        potential_edge = random.choice(edges)
        while rand_weight > potential_edge[1]:
            potential_edge = random.choice(edges)
            rand_weight = random.random()
        
        return potential_edge[0] 
    def get_inefficency(self, inefficency):
        return inefficency[1]
    #returns a tuple (word,inefficency)
    def get_inefficency_list(self,word_time_list,average):
        index = 0
        slow_word_list = []
        ewpm = 0
        total_rank = 0
        while index < len(word_time_list):
            #the user typed this word more slowly than the average word they wrote
            slow_word = word_time_list[index][0]
            # essentially how slow did we type this word * how useful is it to type fast 
            rank_look = self.rank_lookup[slow_word]
            ewpm += rank_look /word_time_list[index][1][0]
            total_rank += rank_look
            inefficency_scale = (word_time_list[index][1][0] - average) * rank_look
            if word_time_list[index][1][0] > average:
                slow_word_list.append((slow_word,inefficency_scale))
            
            index+=1
        slow_word_list.sort(key=self.get_inefficency,reverse=True)
        ewpm = ewpm * 60/ (5*total_rank )
        return slow_word_list,ewpm 

    def get_weighted_random_word(self):
        random_word_num = random.random() * self.rank_total
        for i in self.word_ranks:
            if i[1] > random_word_num: 
                return i[0]
if __name__ == '__main__':
    words = RecommendWords()
    print(words.get_paragraph([], 1, 30))