
class Node:
    def __init__(self, key):
        self.key = key
        self.exp = (None, None) #stores expansion of a term and keeps track of how many times the term has been expanded as a tuple
        self.left = None
        self.right = None

    def set_vals(self, term, count):
        self.exp = (term, count)

    def get_vals(self):
        return self.exp

class BST:
    def __init__(self):
        self.head = None

    def insert(self, key, dic, num_var):
        newnode = Node(key)
        if self.head == None:
            self.head = newnode
            return self.head
        curr = self.head
        while(curr is not None):
            for i in range(num_var):
                if dic[key[i]] > dic[curr.key[i]]:
                    if curr.right is not None:
                        curr = curr.right
                        break
                    else:
                        curr.right = newnode
                        return curr.right
                elif dic[key[i]] < dic[curr.key[i]]:
                    if curr.left is not None:
                        curr = curr.left
                        break # for loop
                    else:
                        curr.left = newnode
                        return curr.left

    def find(self, key, dic, num_var):
        curr = self.head
        while(curr is not None):
            found = True
            for i in range(num_var):
                if dic[key[i]] != dic[curr.key[i]]:
                    found=False
                if dic[key[i]] > dic[curr.key[i]]:
                    curr = curr.right
                    break
                elif dic[key[i]] < dic[curr.key[i]]:
                    curr = curr.left
                    break

            if found: # found exact match
                return curr
        return False

def toLiteral(term, variables):
    literal_string = ""
    for i in range(len(term)):
        if term[i] == None:
            continue
        literal_string += variables[i]
        if term[i] is 0:
            literal_string += "'"
    return literal_string

def toBinaryList(term_list):
    ret_list = []
    for term in term_list:
        new_term = []
        i = len(term)
        while i > 0:
            if term[i-1] == "'":
                new_term.append(0)
                i -= 2
            else:
                new_term.append(1)
                i -= 1
        new_term.reverse()
        # print('Term:',term,'->',new_term)
        ret_list.append(list(new_term))
    return list(ret_list)


def isLegal(term, allterms, nextLegal, num_var, variables): # check if the term is legal
    if None in term:
        for i in range(num_var):
            if term[i] is None:
                term_1 = list(term)
                term_0 = list(term)
                term_1[i] = 1
                term_0[i] = 0

                return isLegal(term_0, allterms, nextLegal, num_var, variables) and isLegal(term_1, allterms, nextLegal, num_var, variables)
    else:
        if term in allterms:
            conv_term = toLiteral(term, variables)
            if conv_term not in nextLegal:
                nextLegal.append(conv_term)
            return True
    return False

def expand(term, allterms, nextLegal, num_var, variables, bst_tree, dic): # recursively expand the term
    node = bst_tree.find(term, dic, num_var) # check if the term was previously expanded
    if node is not False:
        return node.get_vals()

    decre = 0 # stores maximum number of decrements in variables
    expand_max = term #stores maximal expansion
    
    for i in range(num_var):
        if term[i] is not None:
            node = list(term)
            node[i] = 1 - node[i]
            if isLegal(node, allterms, nextLegal, num_var, variables):
                node = list(term)
                node[i] = None
                temp_out = expand(node, allterms, nextLegal, num_var, variables, bst_tree, dic)
                if decre < 1 + temp_out[1]:
                    decre = 1 + temp_out[1]
                    expand_max = temp_out[0]

    newNode = bst_tree.insert(term, dic, num_var) # add expanded term to BST
    newNode.set_vals(expand_max, decre)
    return (expand_max, decre)

def printNextLegal(next):
    print('Next Legal Terms for Expansion: [', end="")
    for i in range(len(next)):
        x = next[i]
        if i > 0:
            print(",", end=" ")
        print('{' + x + '}', end="")
    print("]")

def comb_function_expansion(func_TRUE, func_DC):
    if len(func_TRUE) == 0:
        return [0]

    variables = [i for i in func_TRUE[0] if i != "'"] # remove the primes
    num_var = len(variables)
    dic = {
        None : 2,
        0 : 0,
        1 : 1
    }

    true_terms = toBinaryList(func_TRUE)
    true_dc = true_terms + toBinaryList(func_DC)

    expand_terms = BST() # the binary search tree to store expansions of previously expanded terms

    maxLegalRegion = []

    for i in range(len(func_TRUE)): # append the expanded terms

        #print('Current term expansion:', func_TRUE[i])
        term = true_terms[i]
        nextLegal = []
        expanded_term = expand(term, true_dc, nextLegal, num_var, variables, expand_terms, dic)
        exp_term = toLiteral(expanded_term[0], variables)
        maxLegalRegion.append(exp_term)
        
        #printNextLegal(nextLegal)
        #print('Expanded Term: {', exp_term + '}\n')

    return maxLegalRegion


#func_TRUE=["a'b'c'd'e'", "a'b'cd'e", "a'b'cde'", "a'bc'd'e'", "a'bc'd'e", "a'bc'de", "a'bc'de'", "ab'c'd'e'", "ab'cd'e'"]
#func_DC=["abc'd'e'", "abc'd'e", "abc'de", "abc'de'"]
# answer=["c'd'e'", "a'b'cd'e", "a'b'cde'", "bc'", "bc'", "bc'", "bc'", "c'd'e'", "ab'd'e'"]

#print(comb_function_expansion(func_TRUE,func_DC))
