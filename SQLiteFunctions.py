import sqlite3 
from MyCIM import *

def create_table(c,table,fkeys,fields,fieldtypes = [], replace = False):
    
    if replace: # then drop table  
                try: 
                    c.execute('DROP TABLE {tn}'.format(tn = table))
                except:
                    pass  
                
    # id and name are always created 
    str = 'id TEXT PRIMARY KEY,name TEXT'
    i = 0
    for f in fields:
        
        if fieldtypes.__len__() > i: 
            ft = fieldtypes[i] 
        else:
            ft = 'REAL' # all columns are real by default 
            
        str += ',{fn} {ft}'.format(fn = f, ft = ft)
         
        i += 1
    
    for f in fkeys:
        str += ',{fn} TEXT'.format(fn = f)
    
    
    try: 
        c.execute('CREATE TABLE {tn} ('.format(tn = table) + str + ')')
    except sqlite3.Error as c:
        print(c) 
        return c 
    return c 
        

#def link_table

# types: {field1:'REAL',field2:'TEXT'}
def insert_row(c,table,d,types):
    debug = False
    # build string
    field_string = '('
    value_string = '(' 
    i = 0
    for f in list(d.keys()):
        if i:
            field_string += ','
            value_string += ','
        field_string += "{0}".format(f)
        #if f in ['name','id']: # these are string fields 
        if types[f] == 'TEXT' :
            value_string += "'{0}'".format(d[f])
        else:
            if type(d[f]) == type(True): # value is boolean 
                if d[f]:
                    value_string += "1"
                else: 
                    value_string += "0" 
            else:    
                value_string += "{0}".format(d[f]) 
        i += 1
    field_string += ')'
    value_string += ')'
    
    if debug:
        print(field_string)
        print(value_string)
    try: 
        c.execute('INSERT INTO {tn} '.format(tn = table) 
                  + field_string + ' VALUES ' + value_string)
    except sqlite3.Error as c: 
        print(table)
        print(field_string)
        print(value_string)
        print(c)
        return c 
    return c


# populate table with all objects in iids list
def populate_table(c,table,iids,l,links):
    
    types = {'id':'TEXT','name':'TEXT'}
    for f in object_fields[table]: 
        types[f] = 'REAL' 
    for f in object_foreign_keys[table]: 
        types[f] = 'TEXT'
        
    
    for iid in iids:
        d = {}
        d['id'] = iid 
        d['name'] = l[iid].name 
        for f in object_fields[table]:
            d[f] = getattr(l[iid], f)
        for f in object_foreign_keys[table]:
            d[f] = links[iid][f]
        insert_row(c, table, d, types)