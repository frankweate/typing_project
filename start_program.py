import os
import sys

import curses
import time
import math
from analyze_word import Word
from recommend_words import RecommendWords
intro_string = """╔════╗────────────╔═╗╔═╗
║╔╗╔╗║────────────║║╚╝║║
╚╝║║╠╣─╔╦══╦╦═╗╔══╣╔╗╔╗╠══╦═╗╔╦══╗
──║║║║─║║╔╗╠╣╔╗╣╔╗║║║║║║╔╗║╔╗╬╣╔╗║
──║║║╚═╝║╚╝║║║║║╚╝║║║║║║╔╗║║║║║╔╗║
──╚╝╚═╗╔╣╔═╩╩╝╚╩═╗╠╝╚╝╚╩╝╚╩╝╚╩╩╝╚╝
────╔═╝║║║─────╔═╝║
────╚══╝╚╝─────╚══╝ press ctrl-c to exit"""

line_length = 80
alpha = 0.85
paragraph_length =30
def main(argv):
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    
    
    word_recommender = RecommendWords()
    
    word_data = []
    try:
        while 1:
            x_val = 0
            y_val = 12
            stdscr.addstr(2,0,intro_string)
            #gets the next paragraph
            paragraph,ewpm = get_paragraph(word_recommender,word_data)
            stdscr.addstr(10,90,"EWPM: "+str(math.trunc(ewpm)))
            for word in paragraph:
                
                stdscr.addstr(y_val,x_val,word)
                x_val+= len(word)+1
                if x_val > line_length:
                    x_val = 0
                    y_val+= 2
                
                   
            curses.curs_set(1)
            
            word_data = iterate_paragraph(stdscr,paragraph)
            stdscr.clear()
    except KeyboardInterrupt:
        stdscr.keypad(0)
        curses.nocbreak()
        curses.echo()
        os.system('clear')
        stdscr.clear()
        curses.endwin()

def iterate_paragraph(stdscr,paragraph):
    x,y = get_cursor_pos(0)
    stdscr.move(x,y)
    word_timer = Word()
    for word in paragraph:

        for current_pos in range(0,len(word)):
            current_char = stdscr.getkey()
            while current_char != word[current_pos]:
                current_char = stdscr.getkey()
                

            y +=1
            stdscr.move(x,y)
        word_timer.update_word_time(word)
        current_char = stdscr.getkey()
        while current_char != " ":
            current_char = stdscr.getkey()
            
        if y >= line_length:
            y = 0
            x+= 2
        else:
            y +=1
        stdscr.move(x, y)
    x,y = get_cursor_pos(0)
    stdscr.move(x, y)
    return word_timer.get_data()
# formats an array of words of length num from the algorithm into an array of lines to be outputted.
def get_paragraph(word_recommender,word_data):
    return word_recommender.get_paragraph(word_data, alpha, paragraph_length)
    
    

def get_cursor_pos(chr):
    return (12 + 2*math.floor(chr/line_length),chr % line_length)

if __name__ == '__main__':
    main(sys.argv[1:])