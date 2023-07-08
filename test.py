# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 23:28:02 2022

@author: nsahu
"""

# from http.client import NotConnected
# from this import d
from operator import truediv
from K_map_gui_tk import *

"""
Class kmap is the wrapper for the tkinter gui.
Usage: kmap(<kmap values in list of list form>)
example for 2 input k-map, kmap([[1,0],[0,0]])
        for 3 input k-map, kmap([[1,0,0,1],[0,0,0,1]])
        for 4 input k-map, kmap([[1,0,0,1],[0,0,0,1],[0,1,0,1],[0,1,0,1]])

To draw the region, use api root.draw_region(x1,y1,x2,y2,"fill colour")
Here x1,y1 is the index for the top left corner of the region
x2,y2 is the index for the bottom right corner of the region.
Fill colour options = ['red', 'blue', 'green', 'yellow']
"""

"""
Sample code for the example given in the slide
"""

# root = kmap([[0,1,1,0], ['x',1,'x',0], [1,0,0,0], [1,'x',0,0]])
# root.draw_region(0,1,1,2,'blue')
# root.draw_region(3,3,0,0,'green')
# root.mainloop()


"""
Sample code for the displaying wrap region
"""
# root = kmap([[0,1,1,0], ['x',1,'x',0], [1,0,0,0], [1,'x',0,0]])
# #root.draw_region(1,3,2,0,'blue')
# root.draw_region(3,0,0,3,'green')
# root.mainloop()

def valid(term):
        universal = {0,1,2,3}
        gawd = [[{0,1},{2,3}],[{3,0},{1,2}]]
        set = universal
        if(len(term) == 2) :
                for i in range(len(term)):
                        if (term[i] != None):
                                set = set.intersection(gawd[i][term[i]])
                if(set == {0,3}):
                        return [3,0]
                return list(set)
        else:
                if(term[0] == None):
                        set = {0,1}
                else:
                        set = {term[0]}
                return list(set)

def is_legal_region(kmap_function,term):
        slice = int((len(term) - 1)/2)
        column = term[:slice+1];row = term[slice+1:]
        valid_column = valid(column);valid_row = valid(row)
        top_left = (valid_row[0],valid_column[0])
        bottom_right = (valid_row[len(valid_row)-1],valid_column[len(valid_column)-1])
        for i in valid_row:
                for j in valid_column:
                        if(kmap_function[i][j] == 0):
                                return (top_left,bottom_right,False)
        return (top_left,bottom_right,True)

k_map = [[0,1,0,0],[1,1,'x',1],[0,1,1,'x'],[1,0,0,'x']]
term = [None,0,None,0]
a = is_legal_region(k_map,term)
root = kmap(k_map)
root.draw_region(a[0][0],a[0][1],a[1][0],a[1][1],'red')
root.mainloop()
print(is_legal_region(k_map,term)[2])
