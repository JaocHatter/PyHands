import math
import time
import cv2 as cv
import mediapipe as mp
import numpy as np
#Pyhands by Jared Orihuela 
#Practica 5 de Fundamentos de la Programación
#esta clase es crucial recordarla, pues cuando se trata de Modelos de DL con manos, los parametros puestos son muy
#recurrentes
#=====================================================================================================================
class DetectorDeManos:
    #parametros establecidos por defecto (modificable a la hora de crear un objeto de la clase DetectorDeManos)
    def __init__(self,mode=False,modelcomplexity=1,maxmanos=2,confdeteccion=0.5,confsegui=0.5):
        self.mode=mode      #Aqui creamos el objeto y lo representamos mediante la variable mode
        self.maxmanos=maxmanos
        self.modelcomplex=modelcomplexity
        self.confdeteccion=confdeteccion
        self.confsegui=confsegui
        self.mpmanos=mp.solutions.hands
        self.manos=self.mpmanos.Hands(self.mode,self.maxmanos,self.modelcomplex,self.confdeteccion,self.confsegui)
        self.dibujo=mp.solutions.drawing_utils
        #esta lista nos va ayudar en la funcion dedos arriba para ir directamente a las yemas o landmarks principales
        #de self.lista 
        self.tip=[4,8,12,16,20]
#=====================================================================================================================
    #Esto es solo para graficar una mano y sus nodos xd
    def encontrarmanos(self,frame,dibujar=True):
        imgcolor=cv.cvtColor(frame,cv.COLOR_BGR2RGB)
        self.resultados=self.manos.process(imgcolor)
        if self.resultados.multi_hand_landmarks:
            for mano in self.resultados.multi_hand_landmarks:
                if dibujar:
                    self.dibujo.draw_landmarks(frame,mano,self.mpmanos.HAND_CONNECTIONS)
                    #llamamos a la funcion HAND conections propio de mediapipe
        #nos retorna un frame pero con las manos dibujadas ;)
        return frame
    def encontrarposicion(self,frame,ManoNum=0,dibujar=True):
        xlista=[]
        ylista=[]
        bbox=[]
        self.lista=[]
        if self.resultados.multi_hand_landmarks:
            miMano=self.resultados.multi_hand_landmarks[ManoNum]
            for index,landmark in enumerate(miMano.landmark):
                #ancho y alto del recuadro que sale en la esquina superior izquierda de mi pantalla xd
                alto,ancho,c=frame.shape
                #print(landmark.x) landmark.x es la dimension normalizada (de 0 a 1 ) la cual al ser multiplicada por 
                #un ancho o alto de tu pantalla ayudará a localizarlo en un pixel en específico ;)
                #print(landmark.y)
                cx,cy=int(landmark.x * ancho),int(landmark.y * alto)
                #agrega la posicion x,y de cada punto de referencia o landmark y lo agrega a una lista
                xlista.append(cx)
                ylista.append(cy)
                self.lista.append([index,cx,cy])
                if dibujar:
                    cv.circle(frame,(cx,cy),5,(0,0,0),thickness=-1)
            xmin,xmax=min(xlista),max(xlista)
            ymin,ymax=min(ylista),max(ylista)
            #bbox solo guarda los puntos maximos  minimos, esto ayudará a graficar un rectangulo que abarque toda nuestra mano
            bbox=xmin,ymin,xmax,ymax
            if dibujar:
                #una vez detecte mi mano, hago un cuadro que la abarque
                cv.rectangle(frame,(xmin-20,ymin-20),(xmax+20,ymax+20),(0,255,0),thickness=2)
        # mi variable "lista" guarda la posición de cada landmark (cada nodo en tus dedos), exactamente de los 21!
        #print(self.lista)
        return self.lista,bbox
    #dedos arriba es una funcion que crea una list 1x5 que se llena de 0's o 1's dependiendo los dedos que tengas
    #levantados!
    def dedosarriba(self):
        dedos=[] 
        #Esta condición indica que si la yema del pulgar(landmark_index=4) está encima del landmark_index=3
        #Este caso es interesante pues cuando estire los dedos de mis manos, el unico dedo el cual su yema se 
        #separe de su landmark anterior,más en el eje X que en el eje Y es el pulgar!
        if self.lista[self.tip[0]][1]>self.lista[self.tip[0]-1][1]:
            dedos.append(1)
        else:
            dedos.append(0)
        #aca voy del indice al meñique
        #y estos al ser estirados se separan respecto al eje Y normalmente
        for id in range(1,5):
            if self.lista[self.tip[id]][2]<self.lista[self.tip[id]-2][2]:
                dedos.append(1)
            else:
                dedos.append(0)
        #retorno mi lista que indica que dedos están levantados [1] o nao [0]
        #print(dedos)
        print(dedos)
        return dedos
    #p1 y p2 son los dedos elegidos que nuestro programa va utilizar como referencia para mover el cursor y hacer click
    #en PYHANDS ELIGIREMOS al indice [la yema de este dedo esta indexificado con el numero 8] 
    # y al del medio [la yema de este dedo está indexificado con el numero 12]
    def distancia(self,p1,p2,frame,dibujar=True,r=15,t=3):
        #Indica punto de referencia especificamente del indice y del medio
        #e itera desde el elemento de posicion 1 al final pues la posicion 1 y 2 pues estos son las cordenadas x,y de estos...
        #indice
        x1,y1=self.lista[p1][1:]
        #medio
        x2,y2=self.lista[p2][1:]
        #current position of x and y
        cx,cy=(x1+x2)//2,(y1+y2)//2
        #(dibujar)#--->dibujar es un boooleano
        if dibujar:
            cv.line(frame,(x1,y1),(x2,y2),(0,0,255),t)
            cv.circle(frame,(x1,y1),r,(0,0,255),cv.FILLED)
            cv.circle(frame,(x2,y2),r,(0,0,255),cv.FILLED)
            cv.circle(frame,(cx,cy),r,(0,0,255),cv.FILLED)
        length=math.hypot(x2-x1,y2-y1)
        return length,frame,[x1,y1,x2,y2,cx,cy]
cap=cv.VideoCapture(0)
detector=DetectorDeManos()
ptiempo=time.time()
#ACÁ SOLO PRUEBO QUE LA CLASE EJECUTE SUS FUNCIONES DE ENCONTRAR LAS MANOS Y ENCONTRAR SUS POSICIONES CORRECTAMENTE

while True:
    c,frame=cap.read()
    frame=detector.encontrarmanos(frame)
    lista,bbox=detector.encontrarposicion(frame)
    #if len(lista)!=0:
    #    print(lista[4])    
    ctiempo=time.time()
    fps=1/(ctiempo-ptiempo)
    ptiempo=ctiempo
    cv.rectangle(frame,(0,0),(400,95),(0,0,0),thickness=cv.FILLED)
    cv.putText(frame,"fps: "+str(int(fps)),(10,70),cv.FONT_HERSHEY_DUPLEX,3,(0,255,0),2)
    cv.imshow("PreVisualizacion",frame)
    k=cv.waitKey(1)
    #si presionas esc...
    if k==27:
        break
cap.release()
cv.destroyAllWindows()