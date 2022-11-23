class SymbolTables:
    def __init__(self):
        self.envs = {'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4, 
                'R0' : 0, 'R1' : 1, 'R2' : 2, 'R3' : 3, 'R4' : 4, 'R5' : 5,
                'R6' : 7, 'R8': 8, 'R9' : 9, 'R10' : 10, 'R11' : 11,
                'R12' : 12, 'R13' : 13, 'R14': 14, 'R15' : 15, 'SCREEN': 16384,
                'KBD': 24576}
        
    def addEntry(self, symbol, address):
        self.envs[symbol] = address

    def contains(self, symbol):
        return symbol in self.envs.keys()
    
    def getAddress(self, symbol):
        return self.envs[symbol]


class LabelTables:
    def __init__(self):
        self.envs = {}
        
    def addEntry(self, label, address):
        self.envs[label] = address

    def contains(self, label):
        return label in self.envs.keys()
    
    def getAddress(self, symbol):
        return self.envs[symbol]