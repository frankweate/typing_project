#This is very similar to the pagerank algorithm and it follows a random walk to find the ranks 
#of each word in the top words freq file.
#In the situation of typing: a word's rank should be given by its own rank + (similar_words_rank*similarity)
import csv
import random
def random_surf(iterations,alpha):
    #takes a while since the file size is over 300MiB
    word_graph = load_graph_file_to_memory()
    #word_list contains the amount of iterations spent on a particular word
    word_list = load_list_file_to_memory()
    popularity = load_initial_popularity_from_memory()
    
    top_popularity = popularity['the'][0]
    current_word = random.choice(word_list)
    #this is the model starting its random surf
    #we dont worry about dangling nodes in this model, since there are none
    for iteration in range(0,iterations):
        popularity[current_word][1]+=1
        if iteration % 10000 == 0:
            print(str(int(10000*iteration/iterations)/100) + "%")
        if random.random() > alpha:
        #we find a random node and start surfing from that
            current_word = random.choice(word_list) 
        #increment the value of the word
        else:
        #we traverse to a connected node 
            current_word_edges = word_graph[current_word]
            
            #this next term represents the weights that we put on this node 
            # popularity and similarity
            edge_weights = []
            word_weight = 0
            new_current_node = None
            if len(current_word_edges) == 0:
                #dangling node
                current_word = random.choice(word_list)
            else:
                for edge in current_word_edges:
                    word_weight += edge[1] * popularity[edge[0]][0]/top_popularity
                    edge_weights.append(word_weight)

                rand = random.random() * word_weight
                for weight in range(0,len(edge_weights)):
                    if rand < edge_weights[weight]:
                        new_current_node = current_word_edges[weight][0]
                        current_word = new_current_node
                        break
                    
    
    make_csv(popularity,word_list)
def load_list_file_to_memory():
    list_file = open('csv_files/top_words_freq.csv','r')
    nodes = []
    for row in csv.reader(list_file):
        nodes.append(row[0])
    list_file.close()
    
    return nodes

def load_initial_popularity_from_memory():
    list_file = open('csv_files/top_words_freq.csv','r')
    words = {}
    for row in csv.reader(list_file):
        words[row[0]] = [int(row[1]),0]
    list_file.close()
    return words

def load_graph_file_to_memory():
    file = open('csv_files/graph.csv','r')
    graph = {}
    for row in csv.reader(file):
        key,edge_list = convert_string_to_edge_list(row)
        graph[key] = edge_list
    file.close()
    return graph
def convert_string_to_edge_list(string):
        name = string[0]
        result = string[1]
        result = result.strip(')][(').split('), (')
        list_tuple = []
        if result[0] == '':
            return name,list_tuple
        for i in result:
            vals = i.strip('\'').split('\', ')
            list_tuple.append((vals[0],float(vals[1])))
        return name,list_tuple

def make_csv(popularity,word_list):
    file = open("csv_files/word_rank.csv",'w')
    writer = csv.writer(file)
    sorted_list = []
    for word in word_list:
        sorted_list.append([word,popularity[word][1]])
    sorted_list.sort(key=get_pop,reverse=True)
    for word in sorted_list:
        writer.writerow((word[0],word[1]))
    file.close()
def get_pop(word):
    return word[1]
if __name__ == '__main__':
    random_surf(100000000,0.85)