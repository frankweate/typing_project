

# Frank Weate 
November 2021 <br>
see [typing_project.pdf](https://github.com/frankweate/typing_project/blob/main/typing_project.pdf) for more detail and images 


# A Typing Algorithm

As someone who has recently
begun to touch type. I saw this as the perfect opportunity to create an
Algorithm to help me learn. Most touch typing tutors online often use
pre-written text files (typing.com) or made up words (keybr.com) to
teach touch typing. While I definitely see both websites as useful
resources, I believe that they are efficient in helping someone to learn
how to touch type, as they help with learning key positioning. However
once someone knows the basics, it is much more useful to focus on a more
algorithmic approach to finding words to type. A recommendation system
that finds words similar to badly typed words could be very beneficial
to someone looking to increase their typing speed.

## Typing efficiency

What constitutes typing efficiently? A common typing measurement is
Words Per Minute (WPM). WPM is in fact a misnomer, as the calculation
does not actually use words at all, but instead uses substitutes a word
for $\frac{characters}{5}$. So if someone typed 1000 characters is 4
minutes, we could calculate their WPM as follows:
$$WPM = \frac{\frac{1000}{4}}{5}$$ therefore $WPM=50$ in this case.
Instead of ignoring words entirely and just looking at random
keystrokes, it is more useful to see how the words that we use impact
our typing speed. For example, someone is their everyday life will type
the word 'useful' much more frequently than they will type the word
'noncom' (a word for a non-commissioned officer). For this reason it
would be much more useful to be able to type \"useful\" quickly instead
of the word \"noncom\". For that reason i would argue that WPM is not a
useful metric for gauging a person's typing speed. Consider a word $w$
from a dictionary of length $d$, let $s_w$ equal the speed required to
type it, and $p_w$ equal its popularity.
$$T_s = \sum_{k=1}^d\frac{s_kp_k}{total(p)}$$ This metric makes more
sense in terms of typing purposes as more common/popular words are
weighted more highly.

## Dataset:

The dataset I used for this project is
[here](https://www.kaggle.com/rtatman/english-word-frequency) and it
\"contains the counts of the 333,333 most commonly-used single words on
the English language web, as derived from the Google Web Trillion Word
Corpus.\" This very useful as it allows for a gauge of the popularity of
each word and thus its usefulness in learning how to type it. However
some words in this data-set were not at all useful, as the dataset is
made from search terms, there are a lot of spelling mistakes such as
\"seach\" and random acronyms \"fft\" (fast Fourier transform), which is
a great algorithm, but the acronym is hardly useful in a typing system.
To resolve this issue I took the intersection of this dataset along with
the unix dictionary found in \"/usr/share/dict/words\". This got rid of
random acronyms and spelling mistakes from the dataset. Leaving only
61,426 words in the dataset, as opposed to 333,333. Meaning that I
removed 81.6% of entries from the kaggle dataset.

## Similarity Between Words

It is useful to know words which are typed similarly to each other for
multiple reasons as it helps with recommending words to type as well as
establishing how popular a word is. To map words based on similarity I
created an adjacency list graph containing words with a similarity of
greater than 0.4 in the dictionary to that word. For example the top 10
words in the adjacency list for the word \"the\" are:

```
the,"[(’thee’, 0.8333333333333334), (’they’, 0.75), (’them’, 0.75), (’then’, 0.75), (’thew’, 0.75), (’he’, 0.6666666666666666), (’there’, 0.6666666666666666), (’these’, 0.6666666666666666), (’theme’, 0.6666666666666666), (’theft’, 0.6666666666666666), )...] 
```


These words all have a distinct similarity with respect to how they are
typed to the word \"the\". Not only is this graph useful for obtaining
the overall rank of all the words in the dataset, but it also helps the
recommendation system find similar words to recommend.

### Why adjacency list

while an adjacency matrix is `O(1)` for retrieving the weight at
$edge_{ij}$, however its space complexity of $O(n^2)$ is an issue. with
61,426 words and assuming a 4 byte edge weight that would take up
$4 \times 61426^2 = 15,092,613,904$ of 15 Gigabytes of space. Along with
this issue, using all that space would be wasteful since the similarity
of words such as \"the\" and \"microscope\" would be compared and stored
in the graph. These words are clearly not similar at all and comparing
their similarity is trivial and not helpful in the functionality of the
program. An adjacency list made much more sense as it takes up less
space and allows for only fairly similar nodes to be connected. The
graph itself is kept in a local file \"graph.csv\" with an array of
offsets being used by the recommendation system to instantly access a
node from the graph. The weights of the graph are defined as the degree
of similarity that word i has with word j. so at row i of the adjacency
list, if j has a high enough similarity to i, an edge of weight
similarity will be added to the graph.

### String Similarity Metric

There are multiple methods to determine the similarity of two strings to
each other:

-   **Hamming distance**: the distance of two strings from each other is
    calculated by adding up the positions that they differ, so the
    hamming distance of \"st**ep**\" and \"st**at**\" is 2. This means
    that the algorithm runs in time $O(n)$ where 'n' is the length of
    the two strings. The two main limitations of this model for our
    purposes is that firstly the string must be of equal size. Secondly
    (and the main problem) is that with this problem, the substrings
    within the strings are more informative of similarity that just
    letter positions. For example when looking at similar strings to
    \"the\", the word \"he\" is much closer to it than the word \"toe\",
    even though both distances would be 1. This is because of the \"he\"
    substring in \"the\" and we must find some way of expressing that
    similarity in our model. An example with bits can be seen below:

    

-   **Levenshtein distance**: The Levenshtein distance works on the
    minimum number of single character insertions, deletions and
    modifications needed to make string1 into string2. To implement this
    requires filling out a $m \times n$ matrix where 'm' and 'n' are the
    two string lengths, so the runtime of this algorithm is
    $O(m \times n)$. It is a more useful metric than Hamming distance
    due to its ability to work with different strings lengths. Like
    Hamming distance however, it still fails to take into account the
    substrings within the string, which is something that needs to be
    taken into account for the similarity two strings when they are
    typed. For example looking at the word \"the\", the word \"tap\" has
    the same Levenshtein distance as the word \"**the**ir\". This model
    clearly does not accurately display the similarity of strings with
    respect to typing. Both algorithms' uses are more focused on finding
    typing mistakes by the user rather than words that are actually
    typed similarly.

-   **Custom formula with Convolution**: For this algorithm the
    similarity between two strings should be based off the amount and
    the length of the substrings within both strings. Convolution was
    used here to find all the substrings within two strings. However due
    to the relatively small string length, the overhead cost of
    implementing a fast fourier transform $O(n\log(n))$ seemed to
    outweigh the benefit it would provide. Therefore an $O(n^2)$ system
    was used, since n (string length) in this case was small, a lot of
    concern should not be placed on the scalability of the algorithm for
    when n is large.

    
    
    

    One thing of note is that when using this convolution method,
    substrings within other substrings were not counted. For example if
    the substring \"ing\" was found,then \"in\",\"ng\",\"i\",\"n\",\"g\"
    were all ignored. Once all the substrings have been found, we need
    to calculate similarity. The actual strings and substrings are not
    help anymore, only their lengths. Let $s_1$ and $s_2$ be the length
    of two strings with a set of the length of substrings $w_n$ with $n$
    elements. $$similarity = \frac{\sum_{k=1}^nw_k^2}{s_1 \times s_2}$$
    This equation for word similarity is very useful. Longer substrings
    within strings suitably compensated by the power of two. Meaning
    that one substring of length five is way more valuable than five
    substrings of length one. Since typing is all about how keystrokes
    are positioned next to each other, this is a very useful feature.

-   One fallback of this method is looking at strings of vastly
    different sizes, that still have common features. For example if we
    compute the similarity of \"theorize\" and \"the\" we get
    $$\frac{3^2 + 1^2}{3 \times 8} = \frac{10}{24}$$ this hardly seems
    like a fair similarity value for the two strings especially when
    considering the fact that \"the\" is the substring within
    \"theorize\" and thus matches it completely. For this reason I
    adjusted the value by taking the $log_e$ of the lengths of each
    string and multiplied it by this factor:
    $$\frac{2}{2 + \log_e(\frac{s_1}{s_2})}$$ so if string one
    substantially smaller than string two, then it will be ranked more
    highly. Although I did not settle on this modified string for
    similarity, it is worth noting that the similarity calculation is in
    need of some polishing in how it works especially when considering
    strings of vastly different size.

### Recommendation:

If a user is slow at typing a word, then it can be assumed that they
will also be slow at typing similar words. And so a typing system that
can give words to practice on based on metrics of other words, could
drastically improve your typing speed. Coupled with taking the
popularity of words into account, this system could make learning how to
type faster much easier.

### Popularity:

the most popular word in the dataset is \"the\", but that does not mean
that it is necessarily the most useful word to know. A less common word
which is more similar to a lot of more common words should, in theory,
be a more useful word to learn. Since learning how to type this word
fast, will also help in typing similar words to it fast. In this case we
find that the word \"in\" is actually the most useful word to know in
the dataset, mainly because of its similarity to so many other words.

## Word Rank:

Just like how webpages are ranked by the pagerank algorithm, the words
in the dataset can be ranked like this as well. The alogrithm is used to
page nodes in a graph by the number and quality of the links that are
pointing to them. as shown below:



With an adjacency list of words, the ranking algorithm takes into
account the degree of similarity between two words along with the
popularity of the word. So the weight given from node a to node b is
given by $similarity \times popularity$ where a higher weight means the
nodes are more closely connected. So **a random surfer** model was
developed to iterate over the graph and find accurate rates for the
words.

## Random Surfer

One way to find the ranking of the words, is to randomly surf the graph.
Since by randomly traversing the graph space, a random surfer will
naturally visit more popular destinations (in this case words) more
often. However this model can lead to issues without some tweaks.

-   **Dangling nodes**: A dangling node is a word which does not have
    any outgoing links to any other words in the graph. How should a
    random surfer tackle this issue?

-   **Disconnected**: A graph might be disconnected or not very well
    connected and thus a random surfer might be stuck in only part of
    the whole graph giving unnecessarily high weights to nodes.

So fix this issue we have an $\alpha$ term, where $1-\alpha$ represents
the probability that a random surfer will teleport to a random node in
the graph. For surfing this graph the $\alpha$ was kept at 0.85. This
allows the whole graph to be suitably explored. As shown below:


With an $\alpha$ of 0.85, there is an 85% chance that the nodes will go
one of the current nodes connections. But there is also a 15% chance
that the node will go to any node in the network (including the current
node and its connections).

### Law of Large Numbers:

This algorithm might seem very chaotic. How could it possibly give
accurate results about anything when so much of it is random? The Law of
Large Numbers states that as the iterations of this algorithm trend
towards infinity. The sampled value equals the expected value. We can
prove this using Chebyshev's inequality.
$$P(|\overline X - \mu| \geq \epsilon) \leq \frac{Var(\overline X)}{\epsilon^2}= \frac{Var(X)}{n\epsilon^2}$$
And as $n$ trends towards infinity the term trends to 0.

### Results of Surfing:

After surfing for many iterations i.e one hundred billion. The word rank
given by the surfer should very closely reflect the ranks of the words.
Unlike with traditional Pagerank that was used on pages on websites, the
landscape of this graph is quite different. Here is a list of the top
twenty-five words found by the algorithm:

```
    in,2996714
    the,2081008
    a,1821925
    and,1362967
    i,1255542
    all,1197426
    is,1136977
    to,1123147
    on,1027609
    at,999468
    an,996782
    as,944560
    or,906364
    it,870291
    for,761940
    are,697984
    that,670956
    be,476380
    e,449694
    this,440784
    re,395011
    of,386790
    see,382558
    us,366126
    s,332346
    can,327143
    will,326362
    one,326130
    he,303469
    here,293988
  ```


Even though in the original kaggle dataset 'the' was listed as the most
popular word, after applying wordrank 'in' was regarded as the most
popular word. This is other high ranking words such as 'line' and 'info'
point to this word, where 'the' has lower ranking words. In total 977
words point to 'in',whereas only 230 point to 'the'.

## Recommendation:

The system now has a ranking of the usefulness of each word through its
wordrank as well as a graph containing the similarity of words. Based
off this information we can identify the importance of a word based off
its rank, if a user is typing an important word very slowly, the system
should highly recommend that word and words similar to it for practice.
Similar to the word rank algorithm above. The Recommendation algorithm
is going to randomly surf the graph. The goal is to find similar words
to the previous under-performing words and recommend those word for the
user the practice.

To get the slower words that have been typed we simply take the average
of all the words that have been typed so far, and subtract that from
that word's time. Clearly if this number is positive it means that the
letters in the word were typed slower than average. The fast words such
as word2 and word1 are ignored, since the algorithm is meant to focus on
slower words. The code then examines the words that are slower than
average and in this case looks at word3, word4 and word5. It then
retrieves the word rank of each slower word to see how useful learning
how to type this word is. The metric used to rank the inefficiency of
learning a word is then calculated:
$$Inefficiency = (wordtime - averagetime) \times wordrank$$ In this case
it is the area of the dashed box shown for each of the words. Meaning
that word4 is the most inefficient word. All three words are then added
to a sorted inefficiency list ranked from most inefficient to least
inefficient. Once a list of inefficient words has been created, similar
words to this inefficient word can be found in the similarity graph. for
example as seen in the graph.csv file:

```
 word,"[(’words’, 0.8), (’sword’, 0.8), (’wordy’, 0.8), (’worded’, 0.7083333333333334), (’reword’, 0.7083333333333334), (’swords’, 0.6666666666666666) ... (’wordsmiths’, 0.4), (’wordlessly’, 0.4), (’catchwords’, 0.4)]" 
```
We take two random words from this list, and add them to the next
paragraph iteration. So if a user under-performed on 'word', then
'swords' and 'catchwords' could be added to the next iteration.



The structure that is being made is essentially a binary search tree. As
the user iterates over more and more paragraphs this tree will keep on
expanding. Essentially honing in on the worst phrases for typing
possible for that specific user , the user will have to type similar
words to 'word' multiple times. Thus improving their typing of that
word. However a problem with this is that it prevents new words from
being explored in the typing system, and only constrains the user to a
very specific subset of words.

### Back to Alpha:

Just like in the word rank algorithm used above, we will use $\alpha$
here again, to make sure that new words are being added for the user to
explore. The goal is to prevent the user from being cluttered with the
same words over and over, and allow the system to accurately find the
worst words in the entire dictionary for them to practice, this is
similar to the 'Exploration vs Exploitation' problem in machine
learning, except in this case it is human learning. With this alpha
variable, the user only sees $(1-\alpha) \times paragraphsize$ of
similar words, and the rest are randomly selected based of their
wordrank. This is another example of the system deliberately favouring
more useful to know words over less useful ones. So what number should
$\alpha$ be? With some trial and error, I estimated alpha to be best at
0.75

### Program Example:



The program begins by getting random words from the dictionary based on
their wordrank. It is fairly obvious from looking at the paragraph that
words with high word-ranks are there such as:


but also uncommon words such as \"contactable\" and \"pylon\". The
program will get roughly half of these nodes based on the user's typing
performance and get 2 similar words for the next paragraph.



(also worth noting that the word list has not been Censored). Since
\"table\" was the worst performing word here, the words \"stabler\" and
\"disable\" are recommended by the system. In this example Shuffle was
turned off, when generally it defaults to on. \"cleanliness\" was second
least performing so \"manliness\" and \"splines\" are recommended and so
on. So all these words appear in the next iteration i.e paragraph.

## Testing:

How should the success of the algorithm be measured? If the algorithm
continually recommends popular and under-performing words for the user
to type, then It is successful. Instead of manually testing the system
based of paragraphs of words. I wrote a testing file to test how
effective system is at recommendations. The file essentially passes in
fake word data about how long a word has taken to be typed. For most
words in the paragraph the time taken was in pythonic terms


`T_w=random.random()+ random.random()+ random.random()`


But the tester finds words with a certain substring e.g. \"end\" and
applies a slightly different time value:


`T_w=1.5+random.random()`


The point is to simulate a user having trouble typing a specific
substring. After simulating the typing in multiple paragraphs the
testing function then returns the percentage of words in the final
paragraph with that specific substring. Here is the result of the
substring \"end\" on 50 iterations:



This is a significant result that was repeatedly occurring when I ran
the program. 57% of the final paragraph had the substring \"end\" in it,
which is huge considering that only 0.83% of the data-set contains words
with the substring \"end\". Keeping in mind this is with an alpha of 1,
next we will explore the effects of changing the alpha on our tester
function.

### Testing alpha:

With a slight modification to the test file and the creation of a
graphing file in python, we can show the percentage of current words
with a substring in it. With alpha equal to one the result is:


When we lower the alpha the graph changes:

Unsurprisingly there is more fluctuation in the lower alpha graph, since
more random nodes are added to the paragraph on each iteration. However
on interesting thing to note is that the percentage increases quite
quickly from the first iteration, this is because the random alpha words
in the list allow for more exploration and thus it finds more words with
the substring in it. Considering that the area underneath the graph
represents the amount of times a user types the substring, both are
fairly effective at making a user type the substring, but the 0.85 alpha
allows for more exploration and helps finds inefficient words faster. As
a comparison this is what the graph looks like when presented with
random words (alpha = 0).

The graph never reaches over the 10% mark at spends over 85% of its
iterations at 0. Further pointing to the algorithm's success at
recommending similar words. This graphing was done with multiple
substrings yielding similar results. Because of these results I decided
to kept the alpha at 0.85.

## Measuring Typing Speed:

Going back to the first page: Consider a word $w$ from a dictionary of
length $d$, let $s_w$ equal the speed required to type it, and $p_w$
equal its popularity. $$T_s = \sum_{k=1}^d\frac{s_kp_k}{total(p)}$$
$p_w$ here can be pretty clearly defined as the wordrank of $w$. With
this we can calculate the effective speed of a paragraph (if the system
has the wordrank of a word along with the time taken to type it). With
this in mind the system now has an EPWM metric.

# Code:

**To run the code just type \"python start_program.py\"** Here is some
code used in the assignment: (Note: I only included the code that
implemented the features talked about above) files not included are
(tester.py, start_program.py, prune_data.py, graph_test.py,
analyze_words.py)

## word_rank.py

this function creates a file called word_rank.csv, full of the word
ranks from the word list.

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

## word_similarity.py

Calculates the similarity of 2 given strings:

    #finds the similarity between 2 words (
    # similarity in terms of typing and not in terms of meaning)
    import math

    def similarity(string1,string2):
    #for this convulution to work we must first add padding  to one of the strings
    #runtime O(n^2)
        similarity = 0
        #get string lengths
        string_length1 =  len(string1)
        string_length2 = len(string2)
        string_length = 0
        padded_string = ""
        non_padded_string = ""
        divisor = string_length2 * string_length1 
        #below variables are being initialized depending on which string is bigger
        if string_length1 > string_length2:
            #divisor = string_length1 * (string_length2 + 1) / 2
            string_length=string_length1+2*(string_length2-1)
            padded_string = string1.center(string_length)
            non_padded_string = string2
        else:
            #divisor = string_length2 * (string_length1 + 1) / 2
            string_length=string_length2+1*(string_length1-1)
            padded_string = string2.center(string_length)
            non_padded_string = string1
        for i in range(0,len(padded_string)):
                similarity+=recurse_string(i,0, padded_string, non_padded_string,0)

        #since padded_string > non_padded_string we divide by the maximum value padded_string can have
        # which is the triangle number of string length
        similarity = similarity / divisor
        return similarity

    def recurse_string(i,j,string1,string2,val):
        if i >= len(string1) or j >= len(string2):
            return 0
        if string1[i] != string2[j]:

            return recurse_string(i+1, j+1,string1, string2, 0)
        else:
            return 1 + 2*val + recurse_string(i+1, j+1, string1, string2,val+1)

## create_similarity_graph.py

This code was only ran to create the similarity graph which is
subsequently stored in a csv file for easy access.

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

## recommend_words.py

Firstly the similarity graph must be made, and then the work rank file.
After this recommend words contains the logic for recommending words for
the next paragraph.

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
                    
            #random.shuffle(paragraph)
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

# Conclusion

## Potential Improvements

-   the user interface is very barebones and uses the terminal control
    library curses. This mainly because the UI was not the focus of the
    project. This could be improved to a client server model running on
    a webpage.

-   currently all the data is stored in csv_files, it would be more
    optimal to store it in databases such as PostgeSQL for
    word_rank.csv, word_list.csv and similarity_graph.csv

-   One additional feature that I thought about implementing but did not
    actually add, is some sort of key positional graph that could be
    used to modify the similarity function of two strings. For example
    \"p\" and \"o\" share a similar location on the keyboard, so
    therefore should be treated more similarly than \"p\" and \"z\" for
    example. I ended up not implementing this, since I'm on the fence
    about if it would add unnecessary complexity to the algorithm and
    its implementation might be shaky.

## What I learnt

-   I learnt a lot about string similarity theory in the process of
    doing this assignment Hamming distance and Levenstein distance we
    only a few metrics I looked at. It is ironic that the lack of a
    suitable algorithm for my purposes forced me to learn a lot on the
    subject.

-   How to implement a pagerank like algorithm was interesting, and
    fairly since the random surfer will accurately find the ranks just
    from increasing iterations as shown by the law of large numbers.

-   a stronger understanding of how the $\alpha$ variable works in a
    pagerank algorithm and the trade-off from having the $\alpha$ too
    high or too low.

-   This was very different from anything I have written before. A lot
    of the implementation was trial and error to see what worked and
    what did not. I think I made 10+ graph.csv files containing
    different weights to see what worked with the wordrank algorithm.

-   Increased my EWPM from 45 to 55 over the course of this assignment,
    partially from typing in the program but also from the typing of
    this report.

::: {.thebibliography}
9 Ignjatovic, A., 2021. DFT, DCT and convolution. \[online\]
Cse.unsw.edu.au. Available at:
http://www.cse.unsw.edu.au/ cs4121/lectures_2019/DFT_DCT_CONV_short.pdf.
Ignjatovic, A., 2021. Google PageRank and Markov Chains. \[online\]
Cse.unsw.edu.au. Available at:
http://www.cse.unsw.edu.au/ cs4121/lectures_2019/pagerank_slides_short.pdf.
Ignjatovic, A., 2021. Recommender Systems. \[online\] Cse.unsw.edu.au.
Available at:
http://www.cse.unsw.edu.au/ cs4121/lectures_2019/recommender_systems_short.pdf\>
\[Accessed 11 November 2021\]. Wu, G., 2021. String Similarity Metrics
-- Edit Distance. \[online\] Available at:
https://www.baeldung.com/cs/string-similarity-edit-distance. Goel, A.,
2021. MS&E 233 Lecture 8: Applications of PageRank to Recommendation
Systems. \[online\] Web.stanford.edu. Available at:
https://web.stanford.edu/class/msande233/handouts/lecture8.pdf.
:::
