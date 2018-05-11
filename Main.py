
from prettytable import PrettyTable
import xml.etree.ElementTree
import re
import math
import sys
import HelpFunctions as hf
from BusBranch import *
from MyCIM import *
from SQLiteFunctions import *
import sqlite3


    
class ParseXMLtoCIM:

    def __init__(self, eq_filepath = '',ssh_filepath = ''):
    
        self.l = {} # empty dictionary containing all equipment objects
        self.links = {} # empty dictionary containing for each object:
        # {field name:ID}
        
        self.eqfile = eq_filepath
        self.sshfile = ssh_filepath
        
    
    def parseEQ(self):
    
        self.tree = xml.etree.ElementTree.parse(self.eqfile)
        self.root = self.tree.getroot()
        
        ## loop over nodes, identify desired elements and create objects ##  
        for child in self.root:
            create_equipment(child,self.l,self.links)
            
        ## link objects
        link_equipment(self.l,self.links)
        
    def parseSSH(self):
    
        self.tree = xml.etree.ElementTree.parse(self.sshfile)
        self.root = self.tree.getroot()
        
        # loop through all nodes, if object exist in l update fields
        for child in self.root:
            update_equipment(child,self.l)
            
        
    def update_id_lists(self):
    
        self.substations = [] # list of substations
        self.voltage_levels = [] # list of voltage levels
        self.machines = [] # list of synchronous machines
        self.base_voltages = [] # base voltages
        self.generating_units = [] # generating_units
        self.regulating_controls = []
        self.power_transformers = []
        self.ratio_tap_changers = []
        self.power_transformers_end = []
        self.breakers = []
        self.energy_consumers = []
        self.ac_line_segments = []
        self.terminals = []
        self.busbar_sections = []
        self.connectivity_nodes = []
        self.linear_shunt_compensators = []
        self.ratio_tap_changers = []
        self.equivalent_injections = []
        self.energy_sources = []
        
        ## create lists with objects of various types ##
        for id in self.l.keys():
            if type(self.l[id]) is registry['Substation']: 
                self.substations.append(id)
            elif type(self.l[id]) is registry['VoltageLevel']:
                self.voltage_levels.append(id)
            elif type(self.l[id]) is registry['SynchronousMachine']:
                self.machines.append(id)    
            elif type(self.l[id]) is registry['BaseVoltage']:
                self.base_voltages.append(id)
            elif type(self.l[id]) is registry['GeneratingUnit']:
                self.generating_units.append(id)
            elif type(self.l[id]) is registry['RegulatingControl']:
                self.regulating_controls.append(id)
            elif type(self.l[id]) is registry['PowerTransformer']:
                self.power_transformers.append(id)
            elif type(self.l[id]) is registry['RatioTapChanger']:
                self.ratio_tap_changers.append(id)
            elif type(self.l[id]) is registry['PowerTransformerEnd']:
                self.power_transformers_end.append(id)
            elif type(self.l[id]) is registry['Breaker']:
                self.breakers.append(id)
            elif type(self.l[id]) is registry['EnergyConsumer']:
                self.energy_consumers.append(id)
            elif type(self.l[id]) is registry['ACLineSegment']:
                self.ac_line_segments.append(id)
            elif type(self.l[id]) is registry['Terminal']:
                self.terminals.append(id)
            elif type(self.l[id]) is registry['BusbarSection']:
                self.busbar_sections.append(id)
            elif type(self.l[id]) is registry['ConnectivityNode']:
                self.connectivity_nodes.append(id)
            elif type(self.l[id]) is registry['LinearShuntCompensator']:
                self.linear_shunt_compensators.append(id)
            elif type(self.l[id]) is registry['RatioTapChanger']:
                self.ratio_tap_changers.append(id)
            elif type(self.l[id]) is registry['EquivalentInjection']:
                self.equivalent_injections.append(id)
            elif type(self.l[id]) is registry['EnergySource']:
                self.energy_sources.append(id)
                
        self.eq_te_map = map_equipment_to_terminals(self.terminals, self.links, self.l)
    


    # create branches, generators, nodes, loads, and shunts
    def create_bus_branch_objects(self, baseMVA = 100):
        debug = False
        self.Sb = baseMVA
        res = group_connectivity_nodes(self.connectivity_nodes, self.terminals, self.eq_te_map, self.links, self.l)
        bus_map = res[0]
        nbus = res[1]
        voltages = res[2]
     
        self.buses = []
        for i in range(0,nbus):
            thisbus = Bus(i+1, bus_type = 1, Vb = voltages[i]) # bus is PQ by default
            # find voltage level of bus
            self.buses.append( thisbus )
           
        self.branches = []
        # transformers and ac_line_segments become branches
        for id in self.ac_line_segments:
            # find first bus
            te1 = self.eq_te_map[id][0]
            cn1 = self.links[te1]['ConnectivityNode']
            bus1 = bus_map[cn1]
            # find second bus
            te2 = self.eq_te_map[id][1]
            cn2 = self.links[te2]['ConnectivityNode']
            bus2 = bus_map[cn2]
            
            branch = Branch(id,bus1,bus2,self.l[id].name)
            
            branch.r = self.l[id].r
            branch.x = self.l[id].x 
            branch.b = self.l[id].bch 
            
            
            if 0: # use line base voltage for pu calculation
                base_voltage = self.l[self.links[id]['BaseVoltage']]
                branch.Vbt = base_voltage.nominalVoltage
            if 1: # use highest bus voltage for pu calculation
                v1 = self.buses[bus1-1].Vb
                v2 = self.buses[bus2-1].Vb 
                branch.Vbt = max([v1,v2])
            
            self.branches.append( branch )
        
        if debug:
            print("Branches from ACLineSegments:")
            print('')
            for b in self.branches:
                hf.printo(b)
                print('')
            
           
        self.transformer_branches = []    
        #print(self.power_transformers.__len__()+self.ac_line_segments.__len__())   
        # Note: Transformers with three connectivity nodes will result in 3 separate
        # branches connecting all three nodes 
        for id in self.power_transformers:
            
            if self.eq_te_map[id].__len__() == 2: # 2 WINDING TRANSFORMER
                # find first bus
                te1 = self.eq_te_map[id][0]
                cn1 = self.links[te1]['ConnectivityNode']
                bus1 = bus_map[cn1]
                # find second bus
                te2 = self.eq_te_map[id][1]
                cn2 = self.links[te2]['ConnectivityNode']
                bus2 = bus_map[cn2]
                
                # find transformer ends 
                tends = find_transformer_ends(id,self.links,self.l)
                    
                v1 = self.l[self.links[tends[0]]['BaseVoltage']].nominalVoltage
                v2 = self.l[self.links[tends[1]]['BaseVoltage']].nominalVoltage    
                
                if v1 > v2:
                    branch = Branch(id,bus2,bus1,self.l[id].name)
    
                    branch.Vbt = v1
                    branch.Vbf = v2
                    branch.r = self.l[tends[0]].r
                    branch.x = self.l[tends[0]].x
                    branch.b = self.l[tends[0]].b 
                elif v1 < v2:
                    branch = Branch(id,bus1,bus2,self.l[id].name)
    
                    branch.Vbt = v2
                    branch.Vbf = v1
                    branch.r = self.l[tends[1]].r
                    branch.x = self.l[tends[1]].x 
                    branch.b = self.l[tends[1]].b
                else:
                    print("Warning: nominalVoltage at transformer ends equal!")
                
                
                self.branches.append( branch )
                self.transformer_branches.append( branch )
                
            elif self.eq_te_map[id].__len__() == 3: # 3 WINDING TRANSFORMER
                
                # Create extra bus. Each leg of transformer becomes branch connecting
                # the bus of this terminal to the new bus. 
                
                # find transformer ends 
                tends = find_transformer_ends(id,self.links,self.l)
                v = []
                for i in range(0,3):
                    v.append(self.l[self.links[tends[i]]['BaseVoltage']].nominalVoltage)
                # find high voltage end, used for pu calculation for all branches
                Vb = max(v) 
                       
                # new bus
                self.buses.append( Bus(nbus+1, bus_type = 1, Vb = Vb ))
                nbus += 1
                    
                bus2 = nbus
                
                for i in range(0,3):
                    
                    te = self.eq_te_map[id][i]
                    tend = tends[i] 
                    cn = self.links[te]['ConnectivityNode']
                    bus1 = bus_map[cn]
                    v1 = self.l[self.links[tend]['BaseVoltage']].nominalVoltage
                    
                    branch = Branch(id,bus2,bus1,self.l[id].name)
                    
                    branch.Vbt = Vb
                    branch.Vbf = v1
                    branch.r = self.l[tend].r
                    branch.x = self.l[tend].x  
                    branch.b = self.l[tend].b
                    
                    self.branches.append( branch )
                    self.transformer_branches.append( branch ) 

            else:
                print("Warning: Transformer has more than 3 connection points!")

        if 0:
            print('Branches from PowerTransformers')
            print('')
            for b in self.transformer_branches:
                hf.printo(b)
                print()
        
        for b in self.branches:
                do_pu_formating(b, self.Sb)

        self.shunts = []
        # shunt compensators become shunt elements 
        for id in self.linear_shunt_compensators:
            te = self.eq_te_map[id][0]
            cn = self.links[te]['ConnectivityNode']
            bus = bus_map[cn]
            
            shunt = Shunt(id,bus,self.l[id].name)
            # find nominal voltage of Voltage level
            vl = find_base_voltages(id, [], self.links, self.l)
            shunt.Vb = self.l[vl[0]].nominalVoltage
            #shunt.bPerSection = self.l[id].bPerSection
            #shunt.gPerSection = self.l[id].gPerSection
            #shunt.sections = self.l[id].sections 
            if type(self.l[id]) is registry['LinearShuntCompensator']:
                shunt.b = self.l[id].bPerSection * self.l[id].sections 
                shunt.g = self.l[id].gPerSection * self.l[id].sections 
        
            self.shunts.append( shunt )
            
        for s in self.shunts: 
            do_pu_formating(s,self.Sb)
        
        if 0:
            print("Shunt elements:")
            print()
            for s in self.shunts:
                hf.printo(s)
                print()
                
        # add shunts to buses
        for s in self.shunts:
            # find bus of shunt 
            self.buses[s.bus-1].GS += s.GS 
            self.buses[s.bus-1].BS += s.BS 
            self.buses[s.bus-1].g += s.gpu 
            self.buses[s.bus-1].b += s.bpu 
        
        self.generators = []
        # synchronous machines become generators  
        for id in self.machines:
            te = self.eq_te_map[id][0]
            cn = self.links[te]['ConnectivityNode']
            bus = bus_map[cn]
            generator = Generator(id,bus, name = self.l[id].name, p = self.l[id].p, q = self.l[id].q)
            # Find VG from voltage level. How to find operating voltage?? -> RegulatingControl
            generator.Vg = self.l[self.links[id]['RegulatingControl']].targetValue
            
            voltages = find_base_voltages(id, [], self.links, self.l)
            generator.Vb = self.l[voltages[0]].nominalVoltage
            
            self.generators.append( generator )
            
        for g in self.generators:
            do_pu_formating(g, self.Sb)
            
        # convert generator buses to PV and put generator voltage in bus 
        pg = []
        for g in self.generators:
            self.buses[g.bus-1].bus_type = 2
            pg.append(g.p)
            self.buses[g.bus-1].VM = g.VG
  
        # make bus with largest generator slack bus
        sidx = self.generators[pg.index(min(pg))].bus 
        self.buses[sidx-1].bus_type = 3

        if 0:
            print('GENERATORS')
            for g in self.generators:
                hf.printo(g) 
                print()
                 
        # energy_consumers become loads 
        self.loads = []
        for id in self.energy_consumers + self.equivalent_injections:
            te = self.eq_te_map[id][0]
            cn = self.links[te]['ConnectivityNode']
            bus = bus_map[cn]
            #load = Load(id,bus,self.l[id].name)
            
            self.loads.append( Load(id,bus,name = self.l[id].name, p = self.l[id].p, q = self.l[id].q) )        
        
        for l in self.loads:
            do_pu_formating(l, self.Sb)
        
        for l in self.loads: 
            self.buses[l.bus-1].PD += l.PD 
            self.buses[l.bus-1].QD += l.QD 
            
            #print(l.bus)
            #print(self.buses[10].PD)
            
        # REMOVE SINGLE BUS ISLANDS
        # NOTE: HENCEFORTH  buses[i].bus_nr == i+1 IS BROKEN
        connected_buses = []
        for i in range(0,nbus):
            # check if bus has branch connected
            for b in self.branches:
                if (b.fbus == i+1 or b.tbus == i+1) and i+1 not in connected_buses:
                    connected_buses.append(i+1)
        
        for i in range(0,nbus):
            if i+1 not in connected_buses:
                del self.buses[get_bus_idx(i+1, self.buses)]
        
        # PUT GENERATOR VOLTAGE INTO GEN BUSES
        
        if 0: # rearrange buses and branches to comply with CIM2Matpower
            #branch_order = [8,7,12,17,4,7,15,21,13,20,1,2,10,5,14,19,18,11,16,3,9]
            branch_order = [11,12,20,5,14,2,6,1,21,13,18,3,9,15,7,19,4,17,16,10,8]
            bus_order = [7,15,10,12,8,1,3,6,2,9,5,17,11,14,4,16]
            
            branch_order = [branch_order[i]-1 for i in range(0,branch_order.__len__())]
            bus_order = [bus_order[i]-1 for i in range(0,bus_order.__len__())]
    
            self.branches = hf.re_arrange(self.branches, branch_order)
            #re_arrange(self.buses, bus_order)
            
        if 0:
            print('ALL branches:')
            i = 1
            for b in self.branches:
                print()
                print('Branch {0}:'.format(i))
                hf.printo(b)
                i += 1
        
    def print_matpower_case(self,file = None):
        
        if not(file is None):
            orig_stdout = sys.stdout
            f = open(file +'.m','w')
            sys.stdout = f
        
            filename = re.split('/',file).pop()
             
            print("function mpc = " + filename)
            print()    
        
        print("mpc.baseMVA = {0};".format(self.Sb))
        print()
        
        # BUS MATRIX 
        mat = []
        print("mpc.bus = [")
        for b in self.buses: 
            #print('A row')
            mat.append(['{0}'.format(b.bus_nr), '{0}'.format(b.bus_type), 
                         '{0}'.format(b.PD), '{0}'.format(b.QD), '{0}'.format(b.GS), '{0}'.format(b.BS),
                         '1','{0}'.format(b.VM),'0','{0}'.format(b.Vb),'1','1.1','0.9'])
        print(hf.format_matrix(mat).replace('None', 'NaN '))
        print("];")
        print()
        
        # BRANCH MATRIX 
        mat = []
        print("mpc.branch = [")
        for b in self.branches: 
            #print("{0} {1} {2} {3} {4} 0 0 0 1 0 1 -360 360".format(b.fbus, b.tbus, b.rpu, b.xpu, b.bpu))
            #print([b.fbus, b.tbus, b.rpu, b.xpu, b.bpu, 0, 0, 0, 1, 0, 1, -360, 360])
            #print('A row')
            mat.append(['{0}'.format(b.fbus), '{0}'.format(b.tbus), 
                        '{0}'.format(b.rpu), '{0}'.format(b.xpu), '{0}'.format(b.bshpu),
                        '0','0','0','1','0','1','-360','360'])
        
        print(hf.format_matrix(mat).replace('None', 'NaN '))
        print("];")
        print()
        
        # GENERATOR MATRIX
        mat = []
        print("mpc.gen = [")
        for b in self.generators: 
            mat.append(['{0}'.format(b.bus),'{0}'.format(b.PG),'{0}'.format(b.QG),
                        '0','0','{0}'.format(b.VG),'{0}'.format(self.Sb),'1','{0}'.format(b.PG),'0'])
        print(hf.format_matrix(mat).replace('None', 'NaN '))
        print("];")
        print()
        
        if not(file is None):
            sys.stdout = orig_stdout       
            f.close()
            
    def compute_y_matrix(self):
        debug = False
        
        nbus = self.buses.__len__()
        G = [] # conductance
        B = [] # susceptance
        for i in range(0,nbus): # row
            grow = []
            brow = []
            for j in range(0,nbus): #column 
                g = 0
                b = 0
                ibus = self.buses[i] 
                jbus = self.buses[j]
                if i == j: # diagonal
                    # shunt element (already added together shunts for bus)
                    if debug:
                        print(i)
                        print(j)
                    g=ibus.g
                    b=ibus.b
                    # loop over lines 
                    for br in self.branches:
                        if (br.tbus == ibus.bus_nr) or (br.fbus == ibus.bus_nr): # line is connected
                            g += br.gpu 
                            b += br.bpu  
                            b += br.bshpu/2           
                else: # off-diagonal
                    # loop over lines 
                    for br in self.branches: 
                        if (br.tbus == ibus.bus_nr and br.fbus == jbus.bus_nr) or (br.fbus == ibus.bus_nr and br.tbus == jbus.bus_nr): # line is connected
                            g -= br.gpu 
                            b -= br.bpu 
                    if debug:
                        print(g)
                        print(b)
                grow.append(g)
                brow.append(b)  
            G.append(grow) 
            B.append(brow) 
        
        return(G,B)
    
    def print_y_matrix(self,file = None):
        
        Y = self.compute_y_matrix() 
        
        G = hf.format_matrix( hf.num2str(Y[0]) )
        B = hf.format_matrix( hf.num2str(Y[1]) ) 
        
        if not(file is None):
            orig_stdout = sys.stdout
            f = open(file +'.m','w')
            sys.stdout = f
        
        print('G = [')
        print(G)
        print('];')
        print()
        
        print('B = [')
        print(B) 
        print('];') 
        print()
        
        print('Y = G + 1i*B;')
        
        if not(file is None):
            sys.stdout = orig_stdout       
            f.close()
        
    def create_sql_database(self,db):
        
        
        conn = sqlite3.connect(db)
        #print(sqlite3.version)
        c = conn.cursor()
        
        # CREATE TABLES
        tnames = list(registry.keys())
        for name in tnames:

            fields = object_fields[name]
            fkeys = object_foreign_keys[name]
            #print(fields)
            c = create_table(c, name, fkeys, fields, replace = True)
            if not type(c) is sqlite3.Cursor:
                c = conn.cursor()

        populate_table(c,'Terminal', self.terminals, self.l, self.links)
        populate_table(c,'BaseVoltage', self.base_voltages, self.l, self.links)
        populate_table(c,'SynchronousMachine', self.machines, self.l, self.links)
        populate_table(c,'GeneratingUnit', self.generating_units, self.l, self.links)
        populate_table(c,'RegulatingControl', self.regulating_controls, self.l, self.links)
        populate_table(c,'PowerTransformer', self.power_transformers, self.l, self.links)
        populate_table(c,'EnergyConsumer', self.energy_consumers, self.l, self.links)
        populate_table(c,'PowerTransformerEnd', self.power_transformers_end, self.l, self.links)
        populate_table(c,'ConnectivityNode', self.connectivity_nodes, self.l, self.links)
        populate_table(c,'LinearShuntCompensator', self.linear_shunt_compensators, self.l, self.links)
        populate_table(c,'ACLineSegment', self.ac_line_segments, self.l, self.links)
        populate_table(c,'VoltageLevel', self.voltage_levels, self.l, self.links)
        populate_table(c,'Substation', self.substations, self.l, self.links)
        populate_table(c,'Breaker', self.breakers, self.l, self.links)
        populate_table(c,'RatioTapChanger', self.ratio_tap_changers, self.l, self.links)
        
        if 0:
            for ob in self.l:
                # find type of object
                tc = None 
                for cl in list(registry.keys()):
                    if type(ob) is registry[cl]:
                        tc = cl 
                # create dictionary with all values by merging 
                d = {}
                #d['id'] = 
            
        # POPULATE TABLES 
        if 0:
            fields = ['ratedS','qPercent']
            d = {}
            id = self.machines[0] 
            d['id'] = id 
            d['name'] = self.l[id].name
            for f in fields:
                d[f] = getattr(self.l[id],f)
            print(insert_row(c, 'SynchronousMachine', d))
    
       
        conn.commit()
        conn.close() 
   
# given list of buses, returns idx of bus with bus_nr       
def get_bus_idx(bus_nr,buses):
    for i in range(0,buses.__len__()):
        if buses[i].bus_nr == bus_nr:
            return i 
    return None      

# print table with all objects in l using keys from thislist                
def print_object_list(thislist,l):
    # use prettytable
    t = PrettyTable(["rdf:ID", "name"])
    for x in thislist:
        t.add_row([x,l[x].name])
    print(t)  

# print object 
def print_object(id,l):

    # find object type
    for name in list(registry.keys()):
        if type(l[id]) is registry[name]:
            ot = name

    print('-----------------')
    print('Type: {0}'.format(ot))
    print('Name: {0}'.format(l[id].name))
    print('ID: {0}'.format(id))
    print()
    # print fields
    for field in object_fields[ot]:
        print(field+': {0}'.format(getattr(l[id],field)))
    print()    
    # print foregin keys
    for field in object_foreign_keys[ot]:
        print(field+': {0}'.format(getattr(l[id],field)))
    
    print('----------------')

    
  
def create_equipment(node,l,links):

    tag = re.sub('^{.*}','',node.tag)
    #print(tag)
    if tag in registry:
    
        # create object
        c = registry[tag]()
        # create dictionary for foreign keys, should have all fields with None
        d = {}
        for field in object_foreign_keys[tag]:
            d[field] = None
            
        
        # loop through all sub-elements, if they are wanted add them to the object
        for e in node:
            subtag = re.sub('^{.*}','',e.tag)
            
            if subtag == "IdentifiedObject.name": # object name
                c.name = e.text
            else:
                field = re.sub('^.*\.','',subtag)
                if field in object_fields[tag]:
                    if e.text == 'false' or e.text == 'true':
                        # boolean
                        setattr(c,field,e.text == 'true')
                    else:
                        # numeric
                        setattr(c,field,float(e.text)) # Note: needs to be changed if other types of fields exist   
                
                if field in object_foreign_keys[tag]:
                    # get id reference from attribute list
                    ls = list(e.attrib.keys())
                    d[field] = re.sub('^#','',e.attrib[ls[0]])
        
        
        # extract ID from attribute dictionary 
        ls = list(node.keys())
        id = node.attrib[ls[0]]

        l[id] = c
        links[id] = d
        return id # return id of object
    else:
        return None
        

def update_equipment(node,l):

    id = re.sub('^#','',node.attrib[list(node.keys())[0]])
    lid = list(l.keys())
    tag = re.sub('^{.*}','',node.tag)
    if id in lid:
        
        for e in node:
            field = re.sub('^{.*}.*\.','',e.tag)
            
            if field in object_fields[tag]:
                # check if data is boolean
                    if e.text == 'false' or e.text == 'true':
                        # boolean
                        setattr(l[id],field,e.text == 'true')
                    else:
                        # numeric
                        setattr(l[id],field,float(e.text))
        return 1
    else:
        return 0   
   

def link_equipment(l,map): # link equipment in l using mappings in map

    lid = list(l.keys())
    for id in lid:
    
        for field in list(map[id].keys()):
            foreign_key = map[id][field]
            # try to find object in l
            if foreign_key in lid:
                # put link to object
                setattr(l[id],field,l[foreign_key])
            #else:
             #   # create new object and put into l
             #   l[foreign_key] = registry[field]()
             #   setattr(l[id],field,l[foreign_key])


def find_substation(l,map,id): # trace object with id to substation (may not work for all objects)
    
    print(type(l[id]))
    if type(l[id]) is registry['Substation']:
        return id
    elif 'Substation' in list(map[id].keys()):
        return find_substation(l,map,map[id]['Substation'])
    elif 'EquipmentContainer' in list(map[id].keys()):
        return find_substation(l,map,map[id]['EquipmentContainer'])
    elif 'ConnectivityNodeContainer' in list(map[id].keys()):
        return find_substation(l,map,map[id]['ConnectivityNodeContainer'])
    else:
        return None
    

# Group ConnectivityNodes into buses. All ConnectivityNodes connected with
# closed breakers are grouped into a single bus.    
def group_connectivity_nodes(nodes,terminals,eq_te_map,links,l):
    debug = False
    # mapping from node id to bus nr
    bus_map = {}
    voltages = []
    next_bus_idx = 1
    current_bus_idx = 1
    
    for id in nodes:
        if not( id in list(bus_map.keys()) ): # then start a new bus
            bus_map[id] = current_bus_idx
            if debug:
                print("BUS {0}:".format(current_bus_idx))
            #print(vl)
            #print(type(l[id]))
            #print('--------------------------')
            #print(id)
            
            # find all nodes connected to this bus
            node_group = find_connected_nodes(id,[],terminals,eq_te_map,links,l)
            for n in node_group:
                bus_map[n] = current_bus_idx
            
            if debug:
                print("First node:")
                print(id)
                print("Connected nodes:")
                print(node_group) 
              
            # find voltage level
            vl = find_base_voltages(id, [], links, l)
            if not( vl == []): 
                # Note: Some connectivity nodes are linked to Line and thus cannot
                # be linked directly to base voltage. However, some equipment 
                # connected to the connectivity node may be linked to base voltage
                voltages.append(l[vl[0]].nominalVoltage)    
            else:
                #print('---------')
                #print(current_bus_idx)
                # loop through CE connected to this CN to find BaseVoltage    
                # find CE list
                ce_list = []
                for t in terminals:
                    if links[t]["ConnectivityNode"] == id:
                        ce_list.append(links[t]["ConductingEquipment"])
                # find BaseVoltage of CE
                # Select lowest voltage of all CE
                #print(ce_list)
                ce_voltages = []
                for ce in ce_list: 
                    vl = find_base_voltages(ce, [], links, l)
                    if not(vl == []):
                        ce_voltages.append(l[vl[0]].nominalVoltage)
                        #print(l[vl[0]].nominalVoltage)
                        #print(l[vl[0]])
                        #print(l[ce])
                        #break
                
                if ce_voltages == []:
                    voltages.append(None)  # if we still can't find voltage
                else:
                    voltages.append(min(ce_voltages)) # select lowest voltage  
                    
            current_bus_idx += 1
            
    return (bus_map,current_bus_idx-1,voltages) 
    
# id - id of this node
# nl - list of connected nodes to be returned
# terminal_list - list of all terminals
# eq_te_map - 1:N map from node to terminals
# links - linked tree            
def find_connected_nodes(id,nl,terminal_list,eq_te_map,links,l):

    if type(l[id]) is registry['ConnectivityNode']:
    
        # add current node to list
        nl.append(id)
    
        for t in eq_te_map[id]:
        
            # check which equipment is connected
            ce = links[t]["ConductingEquipment"]
            if type(l[ce]) is registry["Breaker"]:
                # check if breaker is closed, in that case continue transversion                
                if l[ce].open == False: # breaker is closed
                    # find other terminal connected to breaker
                    if eq_te_map[ce][0] == t:
                        t2 = eq_te_map[ce][1]
                    elif eq_te_map[ce][1] == t:
                        t2 = eq_te_map[ce][0]
                    else:
                        print("Neither of terminals connected to breaker {0} matched current terminal {1}".format(l[ce]['name'],l[t]['name']))

                    # find connectivity node of other terminal
                    cn2 = links[t2]["ConnectivityNode"]
                    # continue search path at new connectivity node (only if node has not been transversed before)
                    if not( cn2 in nl):
                        nl = find_connected_nodes(cn2,nl,terminal_list,eq_te_map,links,l)

    return nl                

# Create dictionary with Equipment id as keys containing lists of 
# all Terminals connected to that Equipment
# Used to map both ConnectivityNode and ConductingEquipment to connected terminals 
def map_equipment_to_terminals(terminals,links,l):
    d = {}
    for n in list(l.keys()):
        if not( type(l[n]) is registry["Terminal"] ):
            d[n] = []

    for t in terminals:
        cnode = links[t]["ConnectivityNode"]
        if not( cnode == None):
            d[cnode].append(t)
            
        ce = links[t]["ConductingEquipment"]
        if not( ce == None):
            #print(ce)
            #print(l[ce])
            d[ce].append(t)
    if 0:
        for idd in list(d.keys()):
            if d[idd].__len__() > 2:
                
                print(l[idd].name)       
                print(type(l[idd]))
    return d
    

# id - id of object for which to return base voltages
# vl - list of base voltages connected to object, to be returned 
# links - dictionary with all object foreign keys  
# l - dictionary with CIM objects     
def find_base_voltages(id,vl,links,l):
    debug = False
    
    if debug:
        print_object(id,l)
        print(vl)
    
    if type(l[id]) is registry['BaseVoltage']:
        vl.append(id)
        return vl
    elif 'BaseVoltage' in links[id]:
        return find_base_voltages(links[id]['BaseVoltage'],vl,links,l)
    elif type(l[id]) is registry['PowerTransformer']:
        tends = find_transformer_ends(id,links,l)
        #print(tends)
        for t in tends:
            vl = find_base_voltages(t,vl,links,l)
        return vl 
    elif "EquipmentContainer" in links[id]:
        return find_base_voltages(links[id]['EquipmentContainer'],vl,links,l)
    elif "ConnectivityNodeContainer" in links[id]:
        return find_base_voltages(links[id]['ConnectivityNodeContainer'],vl,links,l)
    else:
        return vl # return unedited list
        
 
def find_transformer_ends(id,links,l):

    if not( type(l[id]) is registry['PowerTransformer']):
        return None 
    else:
        # loop through all equipment to find transformer ends
        tl = []
        for tid in list(l.keys()):
            if type(l[tid]) is registry['PowerTransformerEnd']:
                if links[tid]['PowerTransformer'] == id:
                    tl.append(tid)
        return tl 


def do_pu_formating(ob,Sb):
    shunt_bug = False
    
    ob.Sb = Sb
    
    if type(ob) is Branch:  
        ob.Vb = ob.Vbt
        ob.Zb = math.pow(ob.Vb,2)/ob.Sb 
        ob.rpu = ob.r / ob.Zb
        ob.xpu = ob.x / ob.Zb 
        if not(ob.b == None):
            ob.bshpu = ob.b * ob.Zb
        else: 
            ob.bshpu = 0   
        # pu admittance 
        ob.bpu = - ob.xpu / (ob.xpu*ob.xpu + ob.rpu*ob.rpu)
        ob.gpu = ob.rpu / (ob.xpu*ob.xpu + ob.rpu*ob.rpu)
                 
    elif type(ob) is Load:
        # process load 
        # note: p, q is already in MVA, no need for processing
        ob.PD = ob.p 
        ob.QD = ob.q 
    
    elif type(ob) is Shunt:
        
        ob.Zb = math.pow(ob.Vb,2) /ob.Sb
        ob.gpu = ob.g * ob.Zb 
        ob.bpu = ob.b * ob.Zb  
        
        if shunt_bug:
            ob.GS = ob.g 
            ob.BS = ob.b 
        else:
            ob.GS = ob.g * math.pow(ob.Vb,2) # consumed active power (MW)
            ob.BS = ob.b * math.pow(ob.Vb,2) # injected reactive power (MVAr)
        
    elif type(ob) is Generator:
        
        ob.PG = -ob.p 
        ob.QG = -ob.q 
        ob.VG = ob.Vg / ob.Vb
        # sort out unrealistic values 
        if ob.VG > 2:
            ob.VG = 1 
        


def main():
    
    
    ## USE Total_MG_T1 FOR VALIDATING CODE ####
    if 0:   
        print('--------------- VALIDATION -----------------') 
        # xml files 
        EQfilepath = "data/Total_MG_T1_EQ_V2.xml"
        SSHfilepath = "data/Total_MG_T1_SSH_V2.xml"
        
        # output files 
        mpcfile = './Total_MG_T1_python'
        #mpcfile = None
    
        yfile = './Total_MG_T1_Ybus'
        #yfile = None
    
     
        s = ParseXMLtoCIM(EQfilepath,SSHfilepath)
        s.parseEQ()
        s.parseSSH()
        s.update_id_lists()
    
        s.create_bus_branch_objects()
        s.print_matpower_case(file = mpcfile)
        if not( mpcfile is None):
            s.print_matpower_case()
            
        s.print_y_matrix(file = yfile)
        if not( yfile is None):
            s.print_y_matrix()
    
    
    ## USE SYSTEM FOR ASSIGNMENT 1 ## 
    if 1:
        print('--------- ASSIGNMENT OUTPUT -----------------')
        EQfile_a1 = "data/MicroGridTestConfiguration_T1_BE_EQ_V2.xml"
        SSHfile_a1 = "data/MicroGridTestConfiguration_T1_BE_SSH_V2.xml"
    
        # output files 
        mpcfile_a1 = './T1_BE_python'
        #mpcfile_a1 = None
    
        yfile_a1 = './T1_BE_Ybus'
        #yfile_a1 = None
    
     
        s1 = ParseXMLtoCIM(EQfile_a1,SSHfile_a1)
        s1.parseEQ()
        s1.parseSSH()
        s1.update_id_lists()
    
        s1.create_bus_branch_objects()
        s1.print_matpower_case(file = mpcfile_a1)
        if not (mpcfile_a1 is None):
            s1.print_matpower_case()
        s1.print_y_matrix(file = yfile_a1)
        if not (yfile_a1 is None):
            s1.print_y_matrix()
    
    # Other stuff
    if 1:         
           
        db = 'cim_database.sqlite'
        s1.create_sql_database(db)
        


            
if __name__ == "__main__":
    main()       