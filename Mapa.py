import tkinter as tk
from tkinter import filedialog
import numpy as np
import math
import io
from io import StringIO

class Mapa:

    def __init__(self, tipo):
        self.minFilCol = 8
        self.maxFilCol = 18             
        self.proporcionMAx = (16/9)   
        
        self.bloqIrrompible = 3  #  representa los bloques irrompibles
        self.bloqRompible = 7    #  representa los bloques rompibles
        self.bloqEnemigo = 2    #  representa los enemigos
        self.bloqAgente = 1      #  representa el agente
        self.bloqSalida = -1     #  representa la puerta de salida
        self.bloqBomba = 9       #  representa las bombas
        
        self.porcentIrrompible = 15
        self.porcentRompible = 15       
        self.porcentEnemigo = 2        
                        
        self.filas = 1
        self.columnas = 1
        
        self.mapa = np.zeros((self.filas, self.columnas))        
        self.rompiblesX = np.array([])
        self.rompiblesY = np.array([])        
        
        # con ellas se guardara la salida aleatoria
        self.salidaPosX = 0  
        self.salidaPosY = 0 
        
        # con ellas se guardara la posiscion inicial del agente en el mapa
        self.agentePosX = 1
        self.agentePosY = 1
        
        # secuncia de creacion
        if (tipo == 0):
            print("mapa random")
            self.crearMapaRandom()            
            
            print("poner muros", end=" ")
            self.ponerMuros()
            
            #print("poner irrompibles aleatorios", end=" ")
            #self.ponerBloques(self.bloqIrrompible, self.porcentIrrompible)
            
            print("poner irrompibles Con patron", end="\n")
            self.ponerBloqIrrompiblesFijos()
            
            print("poner rompibles", end=" ")
            self.ponerBloques(self.bloqRompible, self.porcentRompible)   
        else:           
            print("mapa de archivo")
            self.crearMapaArchivo() 
                  
        print("poner ponerRestriccion")
        self.ponerRestriccion()
        
        print("listar rompibles", end=" ")
        self.listarRompibles()
        
        print("poner enemigos", end=" ")
        self.ponerBloques(self.bloqEnemigo, self.porcentEnemigo)
        
        print("poner agente")
        self.ponerAgente()         
        
        print("crear salida", end=" ")
        self.crearSalidaAleatoria()       
       
        print("Matriz:")       
        self.imprimir()
               
        
    def crearMapaRandom(self):
        self.filas = np.random.random_integers(self.minFilCol, self.maxFilCol)        
        self.columnas = np.random.random_integers(self.minFilCol, (self.filas*self.proporcionMAx)) # proporcion maxima 16/9
        
        # para pruebas con tamaño fijo de mapa
        """  self.filas = 11
        self.columnas = 11 """ 
                
        self.mapa = np.zeros((self.filas, self.columnas))               
        print("tamaño: (", self.filas, " x ", self.columnas, ")")
        
        
    def crearMapaArchivo(self):        
        root = tk.Tk()
        root.withdraw()          
        ruta = filedialog.askopenfilename()
        archivoTexto = open(ruta, "r")
        datos = archivoTexto.read()  
        archivoTexto.seek(0)  # poner cursor al inicio de los datos
                
        # tranforma datos en matriz (tiene un mundo de argumentos)
        self.mapa = np.genfromtxt(StringIO(datos))     
        
        archivoTexto.close()            

        self.filas = len(self.mapa)
        self.columnas = len(self.mapa[0])
        
        print("tamaño: (", self.filas, " x ", self.columnas, ")")
     
    def listarRompibles(self):
        # sacar las coordenadas de los bloques rompibles del mapa   
        print("(x,y):")
        for i in range(self.filas):            
            for j in range(self.columnas):
                if(int(self.mapa[i][j]) == self.bloqRompible):
                    self.rompiblesX = np.append(self.rompiblesX, i)
                    self.rompiblesY = np.append(self.rompiblesY, j)
                    print("(", i, ",", j, ")")
        
        """ print("rompibles (x, y):")
        for i in range(len(self.rompiblesX)):
            print("(", self.rompiblesX[i], ",", self.rompiblesY[i], ")") """
 
            
    def ponerMuros(self):                 
        for i in range(self.columnas):
            self.mapa[0][i] = self.bloqIrrompible
            
        for i in range(self.columnas):
            self.mapa[self.filas-1][i] = self.bloqIrrompible
            
        for i in range(self.filas):
            self.mapa[i][0] = self.bloqIrrompible
            
        for i in range(self.filas):
            self.mapa[i][self.columnas-1] = self.bloqIrrompible
            
        
    def ponerBloques(self, bloque, porcentaje):
        # porcentaje es el porcentaje aprox de bloques X por mapa
        numBloquesAponer = math.ceil((((self.filas-2) * (self.columnas-2))*(porcentaje/100)))       
        contador = 0               
        while contador < numBloquesAponer:
            filasX = np.random.random_integers(1, self.filas-2)
            columnasX = np.random.random_integers(1, self.columnas-2)

            if(self.mapa[filasX][columnasX] == 0):
                self.mapa[filasX][columnasX] = bloque
                contador = contador + 1   
        print(" A poner = ", numBloquesAponer, "/ puestos = ", contador-1)
                                  
                 
                    
    def ponerBloqIrrompiblesFijos(self):
        for i in range(2, self.filas-1):
            for j in range(2, self.columnas-1):
                if (i%2 == 0 and j%2 == 0):
                    self.mapa[i][j] =self.bloqIrrompible
                     
    def ponerAgente(self):
        self.mapa[self.agentePosX][self.agentePosY] = self.bloqAgente
    
    def ponerRestriccion(self):
        self.mapa[2][1] = 0
        self.mapa[3][1] = 0
        self.mapa[4][1] = 0
        
        self.mapa[1][2] = 0
        self.mapa[1][3] = 0
        self.mapa[1][4] = 0
        
                
    def crearSalidaAleatoria(self):        
        posAleatoria = np.random.random_integers(0, len(self.rompiblesX)-1)
        
        self.salidaPosX = self.rompiblesX[posAleatoria]
        self.salidaPosY = self.rompiblesY[posAleatoria]       
        
        print(" -> (",self.salidaPosX,",",self.salidaPosY,")")
    
    def imprimir(self):
        # imprime como matriz    
        print(self.mapa)
        
        # imprime como salida
        """ for i in range(self.filas):
            for j in range(self.columnas):
                print(self.mapa[i][j], " ", end = "")
            print(end="\n") """
   
        
    def getMapa(self):
        return self.mapa
    
    def getPosSalida(self):
        return self.salidaPosX, self.salidaPosY   
    
    def getPosAgente(self):
        return self.agentePosX, self.agentePosY
    
    def getBloqEnemigo(self):
        return self.bloqEnemigo
    
    def getBloqRompible(self):
        return self.bloqRompible
    
    def getBloqIrrompible(self):
        return self.bloqIrrompible
    
    def getBloqSalida(self):
        return self.bloqSalida
    
    def getBloqBomba(self):
        return self.bloqBomba
    
    def getBloqAgente(self):
        return self.bloqAgente
    
    def getRompibles(self):
        return self.rompiblesX, self.rompiblesY
    
        
    
            
        
