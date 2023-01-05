import PYHANDS1 as cdp
import cv2 as cv
import time as time
import mediapipe as mp
#el gozu de pyautoguid
import pyautogui as auto
import ctypes
from numpy import interp
#Estas librerias son para modificar el volumen y conocer las dimensiones de mi pantalla
user32=ctypes.windll.user32
user32.SetProcessDPIAware()
anchocam,altocam=640,480 #estas son las dimensiones de la pequeña pestaña que saldrá cuando empieze el video 
cuadro=25 #será el pixel (cuadro x cuadro)  el inicio de nuestro espacio por donde podremos mover nuestro dedo indice
anchopantalla,altopantalla=user32.GetSystemMetrics(0),user32.GetSystemMetrics(1)
print("ancho: {} , alto: {}".format(anchopantalla,altopantalla))
#uso de variables globales que solo se usan 1 vez no es necesario
#sua=5
pubix,pubiy=0,0 #Posicion xy pasada de nuestro puntero
cubiy,cubiy=0,0 #Posicion xy actual de nuestro puntero  
capture=cv.VideoCapture(0)
capture.set(3,(anchocam)) #Estableciendo limites
print(capture.set(3,(anchocam)))
capture.set(4,(altocam))
print(capture.set(3,(altocam)))
#declaramos nuestra variable detector en la cual insertaremos nuestro frame y así agregaremos 
#varios atributos como funciones propias de la clase
detector=cdp.DetectorDeManos(maxmanos=1,confdeteccion=0.8,confsegui=0.2)
#empezamos con un bucle que cambia a un nuevo frame cada porción pequeña de tiempo (video xd)
pointermode=0
while True:
    #leemos nuestra variable tipo VideoCapture
    boolean,frame=capture.read()
    #frame será nuestra varibale tipo n dimension array! (en este caso de 2 dimensiones)
    #la funcion encontrarmanos te devolverá el mismo frame pero con los puntos de referencia agregados
    frame=detector.encontrarmanos(frame)
    lista,bbox=detector.encontrarposicion(frame) #creamos las listas donde guardaremos las posiciones, serán cruciales
                                                 # a la hora de darle las cordenadas al bot de pyautogui
    if pointermode==0:
        cv.circle(frame,(cuadro,cuadro),6,(0,240,0),thickness=-1)
    elif pointermode==1:
        cv.circle(frame,(cuadro,cuadro),6,(0,0,240),thickness=-1) 
    elif pointermode==2:
        cv.circle(frame,(cuadro,cuadro),6,(255,255,0),thickness=-1)                                          
    if len(lista)!=0:
        #dedo indice
        x1,y1=lista[8][1:]
        #dedo medio
        x2,y2=lista[12][1:]
        cv.rectangle(frame,(cuadro,cuadro),(anchocam-cuadro,altocam-cuadro),(0,0,0),2)
        dedos=detector.dedosarriba()
        if pointermode==0:
            if dedos[1]==1 and dedos[2]==0:
                x3=interp(x1,(cuadro,anchocam-cuadro),(0,anchopantalla))
                y3=interp(y1,(cuadro,altocam-cuadro),(0,altopantalla))
                #ctime=time.time()
                #fps=ctime-ptime
                cubix=pubix+(x3-pubix)/2.5
                cubiy=pubiy+(y3-pubiy)/2.5
                pubix,pubiy=cubix,cubiy
                cv.circle(frame,(x1,y1),10,(0,0,0),cv.FILLED)
                #ptime=ctime
                #AHORA QUE YA TENGO LAS CORDENADAS, DARLE LAS ORDENEDES A LA COMPUTADORA Xd
                auto.moveTo(anchopantalla-cubix,cubiy)
            elif dedos[1]==1 and dedos[2]==1:
                longitud,frame,linea=detector.distancia(8,12,frame)
                if longitud<30:
                    cv.circle(frame,(linea[4],linea[5]),10,(255,255,0),cv.FILLED)
                    auto.click()
                    time.sleep(0.1)
            elif dedos[0]==0 and dedos[1]==0 and dedos[2]==0 and dedos[3]==0 and dedos[4]==1:
                pointermode+=1
                pointermode=pointermode%3
                print(pointermode)
                time.sleep(0.5)
        elif pointermode==1:
            if dedos.count(0)==5:
                auto.hotkey("Ctrl","+")
                cv.rectangle(frame,(20,altocam-80),(anchocam+100,altocam-10),(0,0,0),thickness=cv.FILLED)
                cv.putText(frame,"zoom: +",(30,altocam-30),cv.FONT_HERSHEY_DUPLEX,2,(0,255,0),thickness=2)
                time.sleep(0.2)
            elif sum(dedos)==5:
                auto.hotkey("Ctrl","-") 
                cv.putText(frame,"zoom: -",(30,altocam-30),cv.FONT_HERSHEY_DUPLEX,2,(0,255,0),thickness=2)
                cv.rectangle(frame,(20,altocam-80),(anchocam+100,altocam-10),(0,0,0),thickness=cv.FILLED)
                time.sleep(0.2)
            elif  dedos[0]==0 and dedos[1]==0 and dedos[2]==1 and dedos[3]==0 and dedos[4]==0:
                cv.putText(frame,"Fuck u!",(anchocam//2,altocam//2+50),cv.FONT_HERSHEY_DUPLEX,2,(0,255,0),thickness=2)
            elif  dedos[0]==0 and dedos[1]==0 and dedos[2]==0 and dedos[3]==0 and dedos[4]==1:
                pointermode+=1
                pointermode=pointermode%3
                print(pointermode)
                time.sleep(0.5)
        else:
            if  dedos[0]==0 and dedos[1]==0 and dedos[2]==0 and dedos[3]==0 and dedos[4]==1:
                pointermode+=1
                pointermode=pointermode%3
                print(pointermode)
                time.sleep(0.5)
            if lista[4][1]<lista[3][1]:
                auto.press("right")
                time.sleep(.4)
            elif lista[4][1]>lista[3][1]:
                auto.press("left")
                time.sleep(.4)
    cv.imshow("Mouse",frame)
    k=cv.waitKey(1)
    if k==27:
        break
capture.release()
cv.destroyAllWindows()



