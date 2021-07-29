import pygame as pg
import numpy as np
import Mapa as mp
import Enemigos as en
import Agente as ag

class Ventana:   
    
    def __init__(self, tipo):
        pg.init()
        
        #############     parte mapa  ###################
        self.mapaObjeto = mp.Mapa(tipo)        
        self.mapaMatrix = self.mapaObjeto.getMapa()
        
        self.filas = len(self.mapaMatrix)
        self.columnas= len(self.mapaMatrix[0])
        
        self.salidaPos = self.mapaObjeto.getPosSalida()
        
        self.imgAgente = pg.image.load("sprites/16.png")
        self.imgEnemigo = pg.image.load("sprites/11.png")
        self.imgBloqIrrompible= pg.image.load("sprites/10.png")
        self.imgBloqRompible= pg.image.load("sprites/8.png")
        self.imgSuelo = pg.image.load("sprites/6.png")
        self.imgSalida = pg.image.load("sprites/1.png")
        self.imgBomba = pg.image.load("sprites/13.png")
        
        #############     parte Enemigos  ###################
        self.bloqEnemigo = self.mapaObjeto.getBloqEnemigo()
        self.enemigos = en.Enemigos(self.mapaMatrix, self.bloqEnemigo)
        
        #############     parte Agente  ###################        
        self.agente = ag.Agente(self.mapaObjeto) 
        
       
        #############     parte grafica  ###################
        self.tamSprite = 32  # tamaño del sprite png
       
        self.pantalla = pg.display.set_mode(
            (self.columnas*self.tamSprite, self.filas*self.tamSprite))
        
        pg.display.set_caption("Bomberman by Doncel and Ramos")
        
        color = (0, 150, 0)
        clock = pg.time.Clock()
        run = True
        pasoApaso = False  
        while run:
            for event in pg.event.get():
                if (event.type == pg.QUIT):
                    #run = False 
                    quit()
                elif (event.type == pg.KEYDOWN):
                    if (event.key == pg.K_SPACE):
                       self.pausa()
                       
                    if (event.key == pg.K_s):
                        if(pasoApaso):
                            pasoApaso = False
                            pg.display.set_caption("Bomberman by Doncel and Ramos")
                        else:
                            pasoApaso = True
                            pg.display.set_caption("(step by step) Bomberman by Doncel and Ramos")
                
                    if (event.key == pg.K_RIGHT):
                       self.jugar()
                                          
            self.pantalla.fill(color)             
            self.dibujar()    
                               
            if(not pasoApaso):               
                self.jugar()
                clock.tick(1)  # Num de FPS entre mas grande mas rapido     

            pg.display.update() 
                       
        pg.quit()  
        
    def jugar(self):            
        self.enemigos.hacerJugada(self.mapaMatrix)
        self.mapaMatrix = self.enemigos.getMapa()
        
        self.agente.hacerJugada(self.mapaMatrix)
        self.mapaMatrix = self.agente.getMapa()

    
    def pausa(self):
        pausa = True
        pg.display.set_caption("(PAUSADO)")
        while pausa:
            for event in pg.event.get():
                if (event.type == pg.QUIT):
                    #run = False
                    quit()
                elif (event.type == pg.KEYDOWN):
                    if (event.key == pg.K_SPACE):
                       pausa = False
                       pg.display.set_caption("Bomberman by Doncel and Ramos")

    def dibujar(self):
        for i in range(self.filas):
            for j in range(self.columnas):
                if (self.mapaMatrix[i][j] == self.mapaObjeto.getBloqIrrompible()):
                    self.pantalla.blit(self.imgBloqIrrompible, (j*self.tamSprite, i*self.tamSprite))
                    
                if (self.mapaMatrix[i][j] == self.mapaObjeto.getBloqRompible()):
                    self.pantalla.blit(self.imgBloqRompible, (j*self.tamSprite, i*self.tamSprite))
                
                if (self.mapaMatrix[i][j] == self.mapaObjeto.getBloqEnemigo()):
                    self.pantalla.blit(self.imgEnemigo, (j*self.tamSprite, i*self.tamSprite))
                    
                if (self.mapaMatrix[i][j] == self.mapaObjeto.getBloqAgente()):
                    self.pantalla.blit(self.imgAgente, (j*self.tamSprite, i*self.tamSprite))
                
                if (self.agente.getYaEncontreSalida()):
                    self.pantalla.blit(self.imgSalida, (self.salidaPos[1]*self.tamSprite, self.salidaPos[0]*self.tamSprite))
                
       
				
