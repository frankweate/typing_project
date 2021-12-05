import csv
# take the intersection of the unix english dictionary along with the kaggle dataset.
#to filter out any unnecessary words, but also allow us to have accurate word frequencies
input1 = open('csv_files/unigram_freq.csv', 'r')
input2 = open('csv_files/british_english.csv','r')
output = open("csv_files/top_words_freq.csv","w")
writer = csv.writer(output)
kaggle_wordlist = set()
english_wordlist = set()
for row in csv.reader(input1):
    kaggle_wordlist.add(row[0])

for row in csv.reader(input2):
    english_wordlist.add(row[0])

intersection = english_wordlist.intersection(kaggle_wordlist)
print(len(intersection))
input1.seek(0)
for row in csv.reader(input1):
    
    if row[0] in intersection:
        writer.writerow(row)
        

input1.close()
input2.close()
output.close()