from word_similarity import similarity
import csv
def create_graph():
    word_freq = open("csv_files/top_words_freq.csv","r")
    reader = csv.reader(word_freq)
    word_list = []
    for row in reader:
        word_list.append((row[0],row[1]))
    word_freq.close()
    graph = {}
    flag = 0
    for i in word_list:        
        graph[i[0]] = list()
        flag+=1
        if flag %10 == 0:
            print(flag)
        for j in word_list:
            if i[0] != j[0]:
                add_to_list(200, graph[i[0]], j[0], similarity(i[0], j[0]))
    output = open("csv_files/graph.csv","w")
    writer = csv.writer(output)
    for key, value in graph.items():
        print(key, value)
        writer.writerow((key,value))
    output.close()
#determines whether to add element to the adajancy list
def add_to_list(length, list, element, similarity):
    add_sorted(element, list, similarity)
    
def add_sorted(element,list,similarity):
    if similarity >= 0.4:
        for i in range(0,len(list)):
            if float(list[i][1]) < similarity:
                list.insert(i,(element,similarity))
                return
            elif i == len(list) -1:
                list.append((element,similarity))
                return
        if len(list) == 0:
            list.insert(-1,(element,similarity))
if __name__ == '__main__':
    create_graph()