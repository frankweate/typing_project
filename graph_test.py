import matplotlib.pyplot as plt
import numpy as np
import sys
from tester import tester
def plot(argv):
# corresponding y axis values
    substring = argv[0]
    iterations = int(argv[1])
    alpha = float(argv[2])
    x = []
    for i in range(0,iterations):
        x.append(i)
    y = tester(argv)
    
    # plotting the points
    plt.plot(x, y)
    
    # naming the x axis
    plt.xlabel('Iteration')
    # naming the y axis
    plt.ylabel('Percentage of substring words')
    
    # giving a title to my graph
    plt.title('Percentage of substring words over time')
    
    # function to show the plot
    plt.show()


if __name__ == '__main__':
    plot(sys.argv[1:])    