import numpy as np

class Nodo:
    
    def __init__(self, iD, padre, posX, posY, gN, hN, fN):
        
        self.iD = iD
        self.padre = padre # indice de vector o lista donde esta el padre 
        self.posX = posX
        self.posY = posY
        self.gN = gN
        self.hN = hN
        self.fN = fN
        
    def imprimirNodo(self):
        print("id:", self.iD, end=", ")
        print("padre:", self.padre, end=", ")
        print("pos(", self.posX, ",",self.posY,")",  end=", ")
        print("g(n):", self.gN, end=", ")
        print("h(n):", self.hN, end=", ")
        print("f(n):", self.fN)
        print()

      
    def getID(self):
        return self.iD
       
    def getPadre(self):
        return self.padre
    
    def getPosX(self):
        return self.posX
    
    def getPosY(self):
        return self.posY
    
    def getGdeN(self):
        return self.gN
    
    def getHdeN(self):
        return self.hN
    
    def getFdeN(self):
        return self.fN
