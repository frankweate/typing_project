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


def main():
    print(similarity("in", "on"))

if __name__ == '__main__':
    main()