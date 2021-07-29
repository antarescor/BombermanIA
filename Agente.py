import Nodo as nd
import queue as cola
import numpy as np


class Agente:
    
    def __init__(self, mapaObjeto):
        
        self.mapaObjeto = mapaObjeto       
        self.mapaMatrix = mapaObjeto.getMapa()
        
        rompiblesAux = mapaObjeto.getRompibles()
        self.rompiblesX = rompiblesAux[0]
        self.rompiblesY = rompiblesAux[1] 
        
        self.metaRompibleX = 0
        self.metaRompibleY = 0
        
        self.yaEncontreSalida = False
        self.metaFinalX = 0
        self.metaFinalY = 0
        
        posAgenteAux = mapaObjeto.getPosAgente()
        self.posAgenteX = posAgenteAux[0]
        self.posAgenteY = posAgenteAux[1]
        
        self.nodoPadre = 0
               
        self.colaPrioridad = cola.PriorityQueue()
        self.colaPrioridadLista = []
        
        self.bloqIrrompible = mapaObjeto.getBloqIrrompible()
        self.bloqRompible = mapaObjeto.getBloqRompible()
        self.bloqEnemigo = mapaObjeto.getBloqEnemigo()  
        self.bloqSalida = mapaObjeto.getBloqSalida()
        self.bloqBomba = mapaObjeto.getBloqBomba()
        
        ##########  variables de costos ########## 
        
        self.costosBloques = {self.bloqIrrompible: 1000,
                              self.bloqRompible: 10, 
                              self.bloqEnemigo: 10000, 
                              1: 0,  #bloque Agente suma  0
                              0: 1}  #bloque Vacio suma 1
                              
        self.acumuladorCostoBloq = 0
        
        self.buscarRompibleMeta()        


    def hacerJugada(self, mapa):  # aca empieza todoooooo
        self.mapaMatrix = mapa
        i = self.posAgenteX
        j = self.posAgenteY
        
        if(len(self.rompiblesX) != 0):
            if(self.mapaMatrix[i-1][j] == self.bloqRompible        # UP
            or self.mapaMatrix[i][j-1] == self.bloqRompible        # LEFT
            or self.mapaMatrix[i][j+1] == self.bloqRompible        # RIGHT
            or self.mapaMatrix[i+1][j] == self.bloqRompible):      # DOWN
                # da la posicion a la que se debe mover el agente
                self.ponerBomba(i, j)               
            else:            
                self.busquedaAgente()
        else:
            print ("fin del juego")
           
    def ponerBomba(self, i, j):        
        if(self.mapaMatrix[i-1][j] != self.bloqIrrompible):  # up
            self.mapaMatrix[i-1][j] = 0            
            if([i-1] == self.mapaObjeto.getPosSalida()[0] and [j] == self.mapaObjeto.getPosSalida()[1]):
                self.yaEncontreSalida = True
                
        
        if(self.mapaMatrix[i][j-1] != self.bloqIrrompible):  # LEFT
            self.mapaMatrix[i][j-1] = 0
            if([i] == self.mapaObjeto.getPosSalida()[0] and [j-1] == self.mapaObjeto.getPosSalida()[1]):
                self.yaEncontreSalida = True
                
        
        if(self.mapaMatrix[i][j+1] != self.bloqIrrompible):  # RIGHT
            self.mapaMatrix[i][j+1] = 0
            if([i] == self.mapaObjeto.getPosSalida()[0] and [j+1] == self.mapaObjeto.getPosSalida()[1]):
                self.yaEncontreSalida = True
                
        if(self.mapaMatrix[i+1][j] != self.bloqIrrompible):  # DOWN
            self.mapaMatrix[i+1][j] = 0
            if([i+1] == self.mapaObjeto.getPosSalida()[0] and [j] == self.mapaObjeto.getPosSalida()[1]):
                self.yaEncontreSalida = True
                     
            
        self.actualizarRompibles()
        if(len(self.rompiblesX) != 0):
            self.buscarRompibleMeta()
        
    def actualizarRompibles(self):        
        self.rompiblesX = np.array([])
        self.rompiblesY = np.array([])
        
        filas = len(self.mapaMatrix)
        columnas = len(self.mapaMatrix[0])
        
        for i in range(filas):
            for j in range(columnas):
                if(int(self.mapaMatrix[i][j]) == self.bloqRompible):
                    self.rompiblesX = np.append(self.rompiblesX, i)
                    self.rompiblesY = np.append(self.rompiblesY, j)
     
    def busquedaAgente(self):   
        self.colaPrioridad = cola.PriorityQueue()
        self.colaPrioridadLista = []
        self.colaDeNodos = []
        
        contIndex = 0        
        iD = contIndex
        padre = -1
        gN = 0
        hN = 0
        fN = gN + hN
        nodoRaiz = nd.Nodo(iD, padre, self.posAgenteX, self.posAgenteY, gN, hN, fN)
        
        self.encolarNodo(fN, nodoRaiz)
        
        condicion = True        
        
        while (condicion):
            indexNodoMenorPadre = int(self.colaPrioridad.get()[1])
            print()
            print() 
                                  
            nodoMenorPadre = self.colaPrioridadLista[indexNodoMenorPadre]
            
            print("nodo Menor Padre ", nodoMenorPadre.getID(), ": ", end="")
            print("pos(", nodoMenorPadre.getPosX(), ",", nodoMenorPadre.getPosY(), ")")
            
            i = int(nodoMenorPadre.getPosX())
            j = int(nodoMenorPadre.getPosY())
            
            if(self.mapaMatrix[i-1][j] == self.bloqRompible           # UP
               or self.mapaMatrix[i][j-1] == self.bloqRompible        # LEFT
               or self.mapaMatrix[i][j+1] == self.bloqRompible        # RIGHT
               or self.mapaMatrix[i+1][j] == self.bloqRompible):      # DOWN
                condicion = False
                self.getJugada(nodoMenorPadre)  # da la posicion a la que se debe mover el agente
            else:
                tipoBloque = int(self.mapaMatrix[i-1][j])  # UP
                if(tipoBloque != self.bloqIrrompible):
                    contIndex = contIndex + 1                    
                    iD = contIndex
                    padre = nodoMenorPadre.getID()
                    x = i-1
                    y = j                    
                    gN = nodoMenorPadre.getGdeN() + self.costosBloques[tipoBloque]
                    hN = self.calcularManhatanAMeta(x, y)
                    fN =  gN + hN
                    
                    nodoAuxiliar = nd.Nodo(iD, padre, x, y, gN, hN, fN)
                    self.encolarNodo(fN, nodoAuxiliar)
                    
                    print("Nodo encolado = ", end=" ")
                    nodoAuxiliar.imprimirNodo()
                
                tipoBloque = int(self.mapaMatrix[i][j-1])  # LEFT
                if(tipoBloque != self.bloqIrrompible):
                    contIndex = contIndex + 1
                    iD = contIndex
                    padre = nodoMenorPadre.getID()
                    x = i
                    y = j-1
                    gN = nodoMenorPadre.getGdeN() + self.costosBloques[tipoBloque]
                    hN = self.calcularManhatanAMeta(x, y)
                    fN = gN + hN

                    nodoAuxiliar = nd.Nodo(iD, padre, x, y, gN, hN, fN)
                    self.encolarNodo(fN, nodoAuxiliar)
                    
                    print("Nodo encolado = ", end=" ")
                    nodoAuxiliar.imprimirNodo()
                
                tipoBloque = int(self.mapaMatrix[i][j+1])  # RIGHT
                if(tipoBloque != self.bloqIrrompible):
                    contIndex = contIndex + 1                    
                    iD = contIndex
                    padre = nodoMenorPadre.getID()
                    x = i
                    y = j+1                    
                    gN = nodoMenorPadre.getGdeN() + self.costosBloques[tipoBloque]
                    hN = self.calcularManhatanAMeta(x, y)
                    fN =  gN + hN
                    
                    nodoAuxiliar = nd.Nodo(iD, padre, x, y, gN, hN, fN)
                    self.encolarNodo(fN, nodoAuxiliar) 
                    
                    print("Nodo encolado = ", end=" ")
                    nodoAuxiliar.imprimirNodo()
                
                tipoBloque = int(self.mapaMatrix[i+1][j])  # DOWN
                if(tipoBloque != self.bloqIrrompible):
                    contIndex = contIndex + 1                    
                    iD = contIndex
                    padre = nodoMenorPadre.getID()
                    x = i+1
                    y = j                    
                    gN = nodoMenorPadre.getGdeN() + self.costosBloques[tipoBloque]
                    hN = self.calcularManhatanAMeta(x, y)
                    fN =  gN + hN
                    
                    nodoAuxiliar = nd.Nodo(iD, padre, x, y, gN, hN, fN)
                    self.encolarNodo(fN, nodoAuxiliar) 
                    
                    print("Nodo encolado = ", end=" ")
                    nodoAuxiliar.imprimirNodo()
        
        print("fin de movimiento")
                    
    def  encolarNodo(self, fN, nodoAuxiliar):
        self.colaPrioridadLista.append(nodoAuxiliar)
        self.colaPrioridad.put((fN, int(nodoAuxiliar.getID())))         
                
    def getJugada(self, nodoAux):
        
        if(self.yaEncontreSalida):
            nuevaPosX = int(self.mapaObjeto.getPosSalida()[0])
            nuevaPosY = int(self.mapaObjeto.getPosSalida()[1])    
        else:                    
            padre = int(nodoAux.getPadre())
            
            while(padre != 0):
                index = padre
                nodoAux = self.colaPrioridadLista[index]
                padre = int(nodoAux.getPadre())
            
            nuevaPosX = int(nodoAux.getPosX())
            nuevaPosY = int(nodoAux.getPosY())

        print("movimiento a hacer (", nodoAux.getPosX(), ",", nodoAux.getPosY(), ")")
        
        self.mapaMatrix[nuevaPosX][nuevaPosY] = 1
        self.mapaMatrix[self.posAgenteX][self.posAgenteY] = 0
        self.posAgenteX = nuevaPosX
        self.posAgenteY = nuevaPosY 
           
    def buscarRompibleMeta(self):
        print()
        print("distancias:")   
        
        fdeN = self.calcularManhatan(0) + self.calcularCostoARompible(0) 
        print("(",self.rompiblesX[0],",",self.rompiblesY[0],") -> F(n) = ", fdeN)
        print()
        self.metaRompibleX = self.rompiblesX[0]
        self.metaRompibleY = self.rompiblesY[0]
            
        minimo = fdeN
             
        for i in range(1,len(self.rompiblesX)):
            fdeN = self.calcularManhatan(i) + self.calcularCostoARompible(i) 
            print("(",self.rompiblesX[i],",",self.rompiblesY[i],") -> F(n) = ", fdeN)
            print()        
            
            if(fdeN < minimo):
                minimo = fdeN
                self.metaRompibleX = self.rompiblesX[i]
                self.metaRompibleY = self.rompiblesY[i]
        
        print("rompible mas viable (", self.metaRompibleX, ",", self.metaRompibleY, ")", end=" ")
        print("f(n) minimo = ", minimo)    
  
       
    def calcularManhatan(self, index):
        manhatan = abs(self.posAgenteX - self.rompiblesX[index]) + abs(self.posAgenteY - self.rompiblesY[index])        
        print("Agente(", self.posAgenteX, ",", self.posAgenteY,")", end=" -> ")
        print("(",self.rompiblesX[index],",",self.rompiblesY[index], ") -> g(n) = ", manhatan)
        return manhatan 
    
    def calcularManhatanAMeta(self, posX, posY):
        manhatan = abs(posX - self.metaRompibleX) + abs(posY - self.metaRompibleY)
        print("nodo Evaluado(", posX, ",", posY,")", end=" -> ")
        print("(",self.metaRompibleX,",",self.metaRompibleY, ") -> g(n) = ", manhatan)
        return manhatan
        
    
    def calcularCostoARompible(self, index):       
        i = int(self.rompiblesX[index])
        j = int(self.rompiblesY[index])
        
        # I
        if (i <= self.posAgenteX and j >= self.posAgenteY):            
            ruta1 = self.sumarRuta1(self.posAgenteX, self.posAgenteY, i, j, -1, 1)
            ruta2 = self.sumarRuta2(self.posAgenteX, self.posAgenteY, i, j, 1, -1)
        
        # II
        elif (i > self.posAgenteX and j >= self.posAgenteY):            
            ruta1 = self.sumarRuta1(self.posAgenteX, self.posAgenteY, i, j, 1, 1)
            ruta2 = self.sumarRuta2(self.posAgenteX, self.posAgenteY, i, j, 1, 1)
        
        # III
        elif (i > self.posAgenteX and j < self.posAgenteY):           
           ruta1 = self.sumarRuta1(self.posAgenteX, self.posAgenteY, i, j, 1, -1)
           ruta2 = self.sumarRuta2(self.posAgenteX, self.posAgenteY, i, j, -1, 1)
        
        # IV
        elif (i <= self.posAgenteX and j < self.posAgenteY):            
            ruta1 = self.sumarRuta1(self.posAgenteX, self.posAgenteY, i, j, -1, -1)
            ruta2 = self.sumarRuta1(self.posAgenteX, self.posAgenteY, i, j, -1, -1)
            
        print("Agente(", self.posAgenteX, ",", self.posAgenteY,")", end=" -> ")
        print("(",self.rompiblesX[index],",",self.rompiblesY[index], ") -> ruta1 h(n) = ", ruta1)
        
        print("Agente(", self.posAgenteX, ",", self.posAgenteY,")", end=" -> ")
        print("(",self.rompiblesX[index],",",self.rompiblesY[index], ") -> ruta2 h(n) = ", ruta2)
        
        if (ruta1<ruta2):
            return ruta1
        else: 
            return ruta2

    def sumarRuta1(self, posInicialX, posInicialY, posFinalX, posFinalY, intervalo1, intervalo2):     
        self.acumuladorCostoBloq = 0
        for i in range(posInicialX, posFinalX+intervalo1, intervalo1):            
            tipoBloque = int(self.mapaMatrix[i][posInicialY])
            self.acumuladorCostoBloq = self.acumuladorCostoBloq + self.costosBloques[tipoBloque]           
            
        for j in range(posInicialY+intervalo2, posFinalY, intervalo2):            
            tipoBloque = int(self.mapaMatrix[posFinalX][j])
            self.acumuladorCostoBloq = self.acumuladorCostoBloq + self.costosBloques[tipoBloque]
        
        return self.acumuladorCostoBloq
    
    def sumarRuta2(self, posInicialX, posInicialY, posFinalX, posFinalY, intervalo1, intervalo2):  
        self.acumuladorCostoBloq = 0
        for j in range(posInicialY, posFinalY+intervalo1, intervalo1):
            tipoBloque = int(self.mapaMatrix[posInicialX][j])
            self.acumuladorCostoBloq = self.acumuladorCostoBloq + self.costosBloques[tipoBloque]
             
        for i in range(posInicialX+intervalo2, posFinalX, intervalo2):            
            tipoBloque = int(self.mapaMatrix[i][posFinalY])
            self.acumuladorCostoBloq = self.acumuladorCostoBloq + self.costosBloques[tipoBloque]           
         
        return self.acumuladorCostoBloq
    
    def getMapa(self):
        return self.mapaMatrix
    
    def getYaEncontreSalida(self):
        return self.yaEncontreSalida
