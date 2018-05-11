  
class Bus:

    def __init__(self, bus_nr, bus_type = None, GS = 0, BS = 0, PD = 0, QD = 0, Vb = None, VM = 1, g=0,b=0):
        self.bus_nr = bus_nr
        self.bus_type = bus_type
        self.GS = GS 
        self.BS = BS 
        self.PD = PD
        self.QD = QD 
        self.Vb = Vb 
        self.VM = VM
        self.g = g 
        self.b = b 
        
class Branch:

    def __init__(self, id , fbus , tbus, name = None, r = None, x = None, b = None):
    
        self.id  = id
        self.fbus = fbus
        self.tbus = tbus 
        self.name = name
        self.r = r
        self.x = x
        self.b = b
    
class Shunt:

    def __init__(self, id, bus, name = None, r = None, x = None):
        self.id = id
        self.bus = bus
        self.name = name
        self.r = r 
        self.x = x 
        
class Generator:

    def __init__(self, id, bus, name = None, p = None, q = None):
        self.id = id
        self.bus = bus
        self.name = name
        self.p = p 
        self.q = q 
        
class Load: 

    def __init__(self, id, bus, name = None, p = None, q = None):
        self.id = id
        self.bus = bus
        self.name = name
        self.p = p 
        self.q = q 