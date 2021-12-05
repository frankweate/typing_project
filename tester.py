#testing the algorithm by creating dummy data and iteratively feeding it through the input
from recommend_words import RecommendWords
import random
import sys
def tester(argv):
    word_recommender = RecommendWords()
    fake_data = []
    if len(argv) < 3:
        print("Usage: [substring] [iterations]")
        return
    keyword = argv[0]
    iterations = int(argv[1])
    alpha = float(argv[2])
    percentage_over_time = []
    for i in range(0,iterations):
        fake_data = get_fake_data(word_recommender.get_paragraph(fake_data, alpha, 30),keyword)
        percentage = 0
        for i in fake_data[0]:
            if keyword in i[0]:
                percentage+=1
        percentage_over_time.append(percentage/30*100)
    print(percentage_over_time)
    return percentage_over_time
def get_fake_data(word_recommender_output,keyword):
    fake_data = [[],0]
    total_random_time  = 0
    for word in word_recommender_output:
        if keyword in word:
            random_time = 1.5 + random.random()
        else:
            random_time = random.random() + random.random() + random.random()
        fake_data[0].append([word,[random_time,1]])
        total_random_time += random_time
    fake_data[1] = total_random_time / len(word_recommender_output)
    fake_data[0].sort(key=sort,reverse=True)
    return fake_data
def sort(element):
    return element[1][0]
if __name__ == '__main__':
    tester(sys.argv[1:])