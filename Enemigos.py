import numpy as np
import math
import io
from io import StringIO

class Enemigos:
    
    def __init__(self, mapaX, bloqEnemigo):
        self.mapa = mapaX 
          
        self.bloqEnemigo = bloqEnemigo
        
        tamaño = self.mapa.shape
        
        self.filMapa = tamaño[0]
        self.colMapa = tamaño[1]
        
        self.posEnemigosX = np.array([])
        self.posEnemigosY = np.array([])
        
        self.posAntEnemigosX = np.array([])
        self.posAntEnemigosY = np.array([])
        
        self.UP = "U"
        self.LEFT = "L"
        self.DOWN = "D"
        self.RIGHT = "R"
        self.SAME = "S" # para enemigos que esten encerrados
        
        self.LIBRE = "O"
        self.NOLIBRE = "X"
        
        self.rutaReglas = "Reglas/ReglasEnemigos.txt"
        
        self.cargarReglas()
        self.reglaAux = np.array([])
        
        self.crearPosEnemigos()
        self.crearPosAnteEnemigos()
        

    def cargarReglas(self): # carga las reglas de un archivo txt        
        archivoTexto = open(self.rutaReglas, "r")
         
        listaFilas = []
        listaColumnas = []
        
        for linea in archivoTexto.readlines():
            listaFilas = []
            for item in linea.strip().split():
                listaFilas.append(item)                
            listaColumnas.append(listaFilas)
        
        print("reglas enemigos")
        self.reglas = np.array(listaColumnas)
        print(self.reglas)
        
        archivoTexto.close()
    
    # guradar direccion de todos los enemigos
    def crearPosEnemigos(self): 
          
        self.posAntEnemigosX = np.array([])
        self.posAntEnemigosY = np.array([])
        
        for i in range(self.filMapa):
            for j in range(self.colMapa):
                if (self.mapa[i][j] == self.bloqEnemigo): # bloque enemigo
                    self.posEnemigosX = np.append(self.posEnemigosX, i)
                    self.posEnemigosY = np.append(self.posEnemigosY, j)

        print("Enemigos (x, y):")
        self.imprimirPosEnemigos(self.posEnemigosX, self.posEnemigosY)
    
    def crearPosAnteEnemigos(self):  # en la primera ejecucion
        
        self.posAntEnemigosX = np.array([])
        self.posAntEnemigosY = np.array([])

        for i in range(len(self.posEnemigosX)):
            
            fil = int(self.posEnemigosX[i])
            col = int(self.posEnemigosY[i])
            
            #arriba
            if (self.mapa[fil-1][col] == 0):  
                self.posAntEnemigosX = np.append(self.posAntEnemigosX, fil-1)
                self.posAntEnemigosY = np.append(self.posAntEnemigosY, col)
                continue

            #izquierda            
            if (self.mapa[fil][col-1] == 0):
                self.posAntEnemigosX = np.append(self.posAntEnemigosX, fil)
                self.posAntEnemigosY = np.append(self.posAntEnemigosY, col-1)
                continue

            #derecha            
            if (self.mapa[fil][col+1] == 0):
                self.posAntEnemigosX  = np.append(self.posAntEnemigosX, fil)
                self.posAntEnemigosY = np.append(self.posAntEnemigosY, col+1)
                continue

            #abajo            
            if (self.mapa[fil+1][col] == 0):
                self.posAntEnemigosX = np.append(self.posAntEnemigosX, fil+1)
                self.posAntEnemigosY = np.append(self.posAntEnemigosY, col)
                continue
            
            self.posAntEnemigosX = np.append(self.posAntEnemigosX, fil)
            self.posAntEnemigosY = np.append(self.posAntEnemigosY, col)
            
        
        print("Enemigos pos Anterior (x, y):")
        self.imprimirPosEnemigos(self.posAntEnemigosX, self.posAntEnemigosY)
            
        
    def imprimirPosEnemigos(self, posX, posY):        
        for i in range(len(posX)):
            print("(", posX[i], ",",posY[i], ")") 
    
    
    def mapearEntorno(self, i):       
        self.reglaAux = np.array([])
        
        fil = int(self.posEnemigosX[i])
        col = int(self.posEnemigosY[i])
               
        #arriba
        # colocar or self.mapa[fil-1][col] == 1 para agente
        if (self.mapa[fil-1][col] == 0 or self.mapa[fil-1][col] == 1 or self.mapa[fil-1][col] == self.bloqEnemigo):
            self.reglaAux = np.append(self.reglaAux, self.LIBRE)
        else:
            self.reglaAux = np.append(self.reglaAux, self.NOLIBRE)

        #izquierda        
        if (self.mapa[fil][col-1] == 0 or self.mapa[fil][col-1] == 1 or self.mapa[fil][col-1] == self.bloqEnemigo):
            self.reglaAux = np.append(self.reglaAux, self.LIBRE)
        else:
            self.reglaAux = np.append(self.reglaAux, self.NOLIBRE)

        #derecha            
        if (self.mapa[fil][col+1] == 0 or self.mapa[fil][col+1] == 1 or self.mapa[fil][col+1] == self.bloqEnemigo):
            self.reglaAux = np.append(self.reglaAux, self.LIBRE)
        else:
            self.reglaAux = np.append(self.reglaAux, self.NOLIBRE)
            
        #abajo
        if (self.mapa[fil+1][col] == 0 or self.mapa[fil+1][col] == 1 or self.mapa[fil+1][col] == self.bloqEnemigo):
            self.reglaAux = np.append(self.reglaAux, self.LIBRE)
        else:
            self.reglaAux = np.append(self.reglaAux, self.NOLIBRE)
            
        #colocar procedencia anterior
        self.reglaAux = np.append(self.reglaAux, self.vengoDe(i))
        
        print("mapeo de (", fil,",", col,") = ", self.reglaAux, end="")
    
    
    def vengoDe(self, i):      
        if(self.posEnemigosX[i]-1 == self.posAntEnemigosX[i] and self.posEnemigosY[i] == self.posAntEnemigosY[i]):
            return self.UP
        
        if(self.posEnemigosX[i] == self.posAntEnemigosX[i] and self.posEnemigosY[i]-1 == self.posAntEnemigosY[i]):
            return self.LEFT
        
        if(self.posEnemigosX[i] == self.posAntEnemigosX[i] and self.posEnemigosY[i]+1 == self.posAntEnemigosY[i]):
            return self.RIGHT
        
        if(self.posEnemigosX[i]+1 == self.posAntEnemigosX[i] and self.posEnemigosY[i] == self.posAntEnemigosY[i]):
            return self.DOWN
        
        return self.SAME
        
    def voyPara(self):
        for j in range(len(self.reglas)):
            a = self.reglaAux
            b = self.reglas[j][0:5]  # para que  no lea el ultimo elemnto
            if ((a == b).all()):
                print(" go --> ", self.reglas[j][5])
                return self.reglas[j][5]
    
    
    def hacerJugada(self, mapa):             
        self.mapa = mapa
        
        """ self.verificarEnemigos() """
        
        for i in range(len(self.posEnemigosX)):           
            self.mapearEntorno(i)            
            destino = self.voyPara()            
            self.moverEnemigos(destino, i)
     
    """ def verificarEnemigos(self):
        
        indexABorrar = []
        
        for m in range(len(self.posEnemigosX)):
            i = int(self.posEnemigosX[m])
            j = int(self.posEnemigosY[m])

            if (int(self.mapa[i][j]) == 0):                
                indexABorrar.append(m)
        
        for i in range(len(indexABorrar)):
            np.delete(self.posEnemigosX, indexABorrar[i])
            np.delete(self.posEnemigosX, indexABorrar[i])

            np.delete(self.posAntEnemigosX,indexABorrar[i])
            np.delete(self.posAntEnemigosX, indexABorrar[i]) """
                 
        
    def moverEnemigos(self, destino, i):
        #actiualizar el historial posAntEnemigos 
        
        filActual = int(self.posEnemigosX[i])
        colActual = int(self.posEnemigosY[i])
        
        filNueva = 0
        colNueva = 0
                  
        if (destino == self.UP):           
            filNueva = filActual-1
            colNueva = colActual
            
        if (destino == self.LEFT):
            filNueva = filActual
            colNueva = colActual-1
        
        if (destino == self.RIGHT):
            filNueva = filActual
            colNueva = colActual+1
            
        if (destino == self.DOWN):
            filNueva = filActual+1
            colNueva = colActual
            
        if(destino == self.SAME):
            filNueva = filActual
            colNueva = colActual
         
        #actualizar posiciones nuevas y anteriores    
        self.posAntEnemigosX[i] = filActual
        self.posAntEnemigosY[i] = colActual   
        
        self.posEnemigosX[i] = filNueva
        self.posEnemigosY[i] = colNueva
            
        #actualizar mapa
        self.mapa[filActual][colActual] = 0 # donde esta pone cero       
        self.mapa[filNueva][colNueva] = self.bloqEnemigo # a donde avanzo pone el enemigo
           
    def getMapa(self): 
        return self.mapa
