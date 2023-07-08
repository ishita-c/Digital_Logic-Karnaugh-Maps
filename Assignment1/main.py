

from K_map_gui_tk import *

def create_gray_code(n):
    if n == 1:
        return ['0', '1']
    else:
        gray_code = create_gray_code(n - 1)
        return ['0' + x for x in gray_code] + ['1' + x for x in reversed(gray_code)]

def check(term, header):
    # term :  list of size k (k is number of inputs)
    # term[i] = 0 / 1 / None [0 / 1/ don't care]
    # header : list of size k
    # header[i] = 0 / 1 / None [0 / 1/ don't care]
    for i in range(len(term)):
        if term[i] != 'x' and term[i] != header[i]:
            return False
    return True

def find_lr(term, cols):
    l, r = 0, 0
    for i in range(len(cols)):
        if check(term, cols[i]):
            l = i
            break

    for i in range(len(cols) - 1, -1, -1):
        if check(term, cols[i]):
            r = i
            break
    # now check if its (l -> r) or (r -> l)
    if l+1 < len(cols) and check(term, cols[l+1]):
        return l, r
    elif l+1 >= len(cols) and not check(term, cols[l-1]):
        return l, r
    else:
        return r, l

def find_tb(term, rows):
    t, b =  0, 0
    for i in range(len(rows)):
        # if rows[i] == term:
        if check(term, rows[i]):
            t = i
            break

    for i in range(len(rows) - 1, -1, -1):
        # if rows[i] == term:
        if check(term, rows[i]):
            b = i
            break
    
    # now check if its (l -> r) or (r -> l)
    if t+1 < len(rows) and check(term, rows[t+1]):
        return t, b
    elif t+1 >= len(rows) and not check(term, rows[t-1]):
        return t, b
    else:
        return b, t

def check_legal(kmap_function, i, j, top, bottom, left, right):
    if top <= bottom and left <= right:
        if top <= i <= bottom and left <= j <= right:
            return not kmap_function[i][j] == 0
    elif top <= bottom:
        if top <= i <= bottom and not (right < j < left):
            return not kmap_function[i][j] == 0
    elif left <= right:
        # return top <= i <= bottom and not (right < j < left) and not kmap_function[i][j] == 0
        if not (bottom < i < top) and left <= j <= right:
            return not kmap_function[i][j] == 0
    else:
        if not (bottom < i < top) and not (right < j < left):
            return not kmap_function[i][j] == 0

    return True

def is_legal_region(kmap_function, term):
    # Check if the term is a legal region
    # term :  list of size k (k is number of inputs)
    # term[i] = 0 / 1 / None [0 / 1/ don't care]

    # return: ((x1, y1), (x2, y2), bool)
    # (x1, y1) : top left corner
    n = len(term)
    rows = create_gray_code(n//2)
    cols = create_gray_code(n - n//2)
    term_row = ""
    term_col = ""
    for i in range(n):
        if i < n - n//2:
            if term[i] is None:
                term_col += "x"
            else:
                term_col += str(term[i])
        else:
            if term[i] is None:
                term_row += "x"
            else:
                term_row += str(term[i])
    # print("term_row= ", term_row)
    # print("term_col= ", term_col)
    left, right = find_lr(term_col, cols)
    top, bottom = find_tb(term_row, rows)
    # print(left, right)
    # print(top, bottom)

    # now check if legal
    nr = len(kmap_function)
    nc = len(kmap_function[0])

    for i in range(nr):
        for j in range(nc):
            if not check_legal(kmap_function, i, j, top, bottom, left, right):
                return ((top, left), (bottom, right), False)
    
    return ((top, left), (bottom, right), True)

# some testing 

# kmapp = [[1, None], [1, 0]]
# print(is_legal_region(kmapp, [0, None]))
# kmapp = [[0,1,1,0], ['x',1,'x',0], [1,0,0,0], [1,'x',0,0]]
# root = kmap(kmapp)
# root.mainloop()

# to check if coordinates are fine
# l = is_legal_region(kmapp, [None, 0, None, 1])
# l = is_legal_region(kmapp, [None, None, None, 0])
# print(l)

################Test Cases################################

#2 variables
#TC1
# kmap_function=[[1,0], ['x',1]]
# root = kmap(kmap_function)
# root.draw_region(0,0,1,1,'blue')
# root.mainloop()
# print(is_legal_region(kmap_function, [None, None]))

#TC2
# kmap_function=[[1,0], ['x',1]]
# root = kmap(kmap_function)
# root.draw_region(0,0,1,0,'blue')
# root.mainloop()
# print(is_legal_region(kmap_function, [0, None]))


#3 variables
# TC1 (corner case)
# kmap_function=[[1,0,1,1], ['x',1,'x',1]]
# root = kmap(kmap_function)
# root.draw_region(0,3,1,0,'blue')
# root.mainloop()
# print(is_legal_region(kmap_function, [None, 0, None]))

#TC2 
# kmap_function=[[1,0,1,1], ['x',1,'x',1]]
# root = kmap(kmap_function)
# root.draw_region(0,1,1,2,'blue')
# root.mainloop()
# print(is_legal_region(kmap_function, [None, 1, None]))

#TC3 
# kmap_function=[[1,0,1,1], ['x',1,'x',1]]
# root = kmap(kmap_function)
# root.draw_region(1,2,1,2,'blue')
# root.mainloop()
# print(is_legal_region(kmap_function, [1, 1, 1]))

#TC4
# kmap_function=[[1,0,1,1], ['x',1,'x',1]]
# root = kmap(kmap_function)
# root.draw_region(1,3,1,0,'blue')
# root.mainloop()
# print(is_legal_region(kmap_function, [None, 0, 1]))


#4 variables
#TC1 (all four corners, 4 variables)
# kmap_function=[[1,1,1,1], ['x',1,'x',0], [1,0,0,0], [1,'x',0,'x']]
# root = kmap(kmap_function)
# root.draw_region(3,3,0,0,'blue')
# root.mainloop()
# print(is_legal_region(kmap_function, [None, 0, None, 0]))

# TC2 
# kmap_function=[[1,1,1,1], ['x',1,'x',0], [1,0,0,0], [1,'x',0,'x']]
# root = kmap(kmap_function)
# root.draw_region(0,0,3,3,'blue')
# root.mainloop()
# print(is_legal_region(kmap_function, [None, None, None, None]))

#TC3
# kmap_function=[[1,1,1,1], ['x',1,'x',1], [1,0,0,1], [1,'x',0,'x']]
# root = kmap(kmap_function)
# root.draw_region(0,3,3,0,'blue')
# root.mainloop()
# print(is_legal_region(kmap_function, [None, 0, None, None]))

#TC4
# kmap_function=[[1,1,1,1], ['x',1,'x',0], [1,0,0,1], [1,'x',0,'x']]
# root = kmap(kmap_function)
# root.draw_region(0,3,1,0,'blue')
# root.mainloop()
# print(is_legal_region(kmap_function, [None, 0, 0, None]))

# #TC5
# kmap_function=[[1,1,1,1], ['x',1,'x',0], [1,0,0,1], [1,'x',0,'x']]
# root = kmap(kmap_function)
# root.draw_region(1,1,2,2,'blue')
# root.mainloop()
# print(is_legal_region(kmap_function, [None, 1, None, 1]))

#TC6
# kmap_function=[[1,1,1,1], ['x',1,'x',0], [1,0,0,1], [1,'x',0,'x']]
# root = kmap(kmap_function)
# root.draw_region(1,1,1,2,'blue')
# root.mainloop()
# print(is_legal_region(kmap_function, [None, 1, 0, 1]))

#TC7
# kmap_function=[[1,1,1,1], ['x',1,'x',0], [1,0,0,1], [1,'x',0,'x']]
# root = kmap(kmap_function)
# root.draw_region(1,1,1,1,'blue')
# root.mainloop()
# print(is_legal_region(kmap_function, [0, 1, 0, 1]))

#TC8
# kmap_function=[[1,1,1,1], ['x',1,'x',0], [1,0,0,1], [1,'x',1,'x']]
# root = kmap(kmap_function)
# root.draw_region(3,1,0,2,'blue')
# root.mainloop()
# print(is_legal_region(kmap_function, [None, 1, None, 0]))
