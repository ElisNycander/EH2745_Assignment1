from pprint import pprint 


# return mylist ordered according to myorder
# note: mylist and myorder must be of equal length
def re_arrange(mylist,myorder):
    return [mylist[i] for i in myorder]


# return nicely formated matrix string
# matrix: [ [c1, c2, ..., cm], [row2], ..., [rown] ]   
def format_matrix(matrix):
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    return '\n'.join(table)
    #print('\n'.join(table))
    
# print all fields of object
def printo(object):
    pprint(vars(object))    

# convert nested list with numbers into string
def num2str(matrix):
    
    if not(type(matrix) is list):
        return "{0}".format(matrix)
    else:
        return [num2str(x) for x in matrix]
