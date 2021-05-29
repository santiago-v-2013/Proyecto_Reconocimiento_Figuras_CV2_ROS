#!/usr/bin/env python

# Librerias


# Se incluyen las librerias necesarias
from __future__ import print_function
 
import roslib
roslib.load_manifest('proyecto')
import sys
import rospy
import cv2
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

# Se definen valores constantes

# Se define el nombre del nodo
NODE_NAME = "formas"

# Se define el nombre de las ventanas donde se mostrara la imagen
SHOW_WINDOW = "Imagen resultado"
FILTERED_WINDOWS = ["Imagen filtrada_1","Imagen filtrada_2"]

# Se define el nombre de los topics 
TOPIC_SUB_IMAGE_IN = "image_input"
TOPIC_PUB_IMAGE_OUT = "imagen_output"


# Se definen las funciones necesarias para identificar color y forma

# Funcion para determinar el color
def figColor(imagenHSV):
# Se ingresa una imagen en formato HSV

  color = ""


  # Se crean los limites de los colores en el formato HSV
  # para posteriormente definir el color
 
  # Rojo
  rojoBajo1 = np.array([0, 100, 20], np.uint8)
  rojoAlto1 = np.array([8, 255, 255], np.uint8)
  rojoBajo2 = np.array([175, 100, 20], np.uint8)
  rojoAlto2 = np.array([179, 255, 255], np.uint8)

  # Naranja
  naranjaBajo = np.array([11, 100, 20], np.uint8)
  naranjaAlto = np.array([19, 255, 255], np.uint8)

  #Amarillo
  amarilloBajo = np.array([20, 100, 20], np.uint8)
  amarilloAlto = np.array([32, 255, 255], np.uint8)

  #Verde
  verdeBajo = np.array([36, 100, 20], np.uint8)
  verdeAlto = np.array([70, 255, 255], np.uint8)

  #Violeta
  violetaBajo = np.array([130, 100, 20], np.uint8)
  violetaAlto = np.array([145, 255, 255], np.uint8)

  #Rosa
  rosaBajo = np.array([146, 100, 20], np.uint8)
  rosaAlto = np.array([170, 255, 255], np.uint8)

  #Azul
  azulBajo = np.array([71, 100, 20], np.uint8)
  azulAlto = np.array([129, 255, 255], np.uint8)

  # se buscan los colores en la imagen, segun los limites altos 
  # y bajos dados mediante las "mask"
  maskRojo1 = cv2.inRange(imagenHSV, rojoBajo1, rojoAlto1)
  maskRojo2 = cv2.inRange(imagenHSV, rojoBajo2, rojoAlto2)
  maskRojo = cv2.add(maskRojo1, maskRojo2)
  maskNaranja = cv2.inRange(imagenHSV, naranjaBajo, naranjaAlto)
  maskAmarillo = cv2.inRange(imagenHSV, amarilloBajo, amarilloAlto)
  maskVerde = cv2.inRange(imagenHSV, verdeBajo, verdeAlto)
  maskVioleta = cv2.inRange(imagenHSV, violetaBajo, violetaAlto)
  maskRosa = cv2.inRange(imagenHSV, rosaBajo, rosaAlto)
  maskAzul = cv2.inRange(imagenHSV, azulBajo, azulAlto)	

  # Se buscan contornos segun el color y de acuerdo a esto posteriormente se evalua que color es
  cntsRojo = cv2.findContours(maskRojo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1] #Reemplaza por 1, si tienes OpenCV3	
  cntsNaranja = cv2.findContours(maskNaranja, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1] #Reemplaza por 1, si tienes OpenCV3
  cntsAmarillo = cv2.findContours(maskAmarillo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1] #Reemplaza por 1, si tienes OpenCV3
  cntsVerde = cv2.findContours(maskVerde, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1] #Reemplaza por 1, si tienes OpenCV3
  cntsVioleta = cv2.findContours(maskVioleta, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1] #Reemplaza por 1, si tienes OpenCV3
  cntsRosa = cv2.findContours(maskRosa, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1] #Reemplaza por 1, si tienes OpenCV3
  cntsAzul = cv2.findContours(maskAzul, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1] #Reemplaza por 1, si tienes OpenCV3
  

  # De acuerdo al numero de contornos se escoge el color 
  if len(cntsRojo)>0: color = "Rojo"
  elif len(cntsNaranja)>0: color = "Naranja"
  elif len(cntsAmarillo)>0: color = "Amarillo"
  elif len(cntsVerde)>0: color = "Verde"
  elif len(cntsVioleta)>0: color = "Violeta"
  elif len(cntsRosa)>0: color = "Rosa"
  elif len(cntsAzul)>0: color = "Azul"

  return color

# Funcion para determinar forma		
def figName(contorno,width,height):

  namefig = ""

  # Se define epsilon, que es la distancia maxima entre el contorno y el contorno aproximado. 
  # Escoger este parametro sabiamente permitira obtener una salida correcta.
  epsilon = 0.01*cv2.arcLength(contorno,True)

  # Aproxima una forma de contorno a otra forma con menos numero de vertices dependiendo de la precision que se especifique. 
  approx = cv2.approxPolyDP(contorno,epsilon,True)

  # De acuerdo a la aproximacion se evalua que figura es y se devulve el nombre
  if len(approx) == 3:
    namefig = "Triangulo"

  if len(approx) == 4:
    aspect_ratio = float(width)/height
    if aspect_ratio == 1:
      namefig = "Cuadrado"
    else:
      namefig = "Rectangulo"

  if len(approx) == 5:
    namefig = "Pentagono"

  if len(approx) == 6:
    namefig = "Hexagono"

  if len(approx) > 8:
    namefig = "Circulo"

  return namefig


# Definicion de la clase
class image_converter:

  # Metodo contructor de la clase, se crea el publicador y el suscriptor
  # Ademas se crea el puente entre ROS y OpenCV
  def __init__(self):
  
    self.image_pub = rospy.Publisher(TOPIC_PUB_IMAGE_OUT,Image)
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber(TOPIC_SUB_IMAGE_IN,Image,self.callback)


  # Callback de la clase
  def callback(self,data):

    # Si desea utilizar la camara descomente las siguientes 4 lineas de codigo

    #try:
    #  cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    #except CvBridgeError as e:
    #  print(e)

    # Si desea leer una imagen guardada descomente la sigueinte linea

    cv_image = cv2.imread('/home/santiago/corte_3/src/proyecto/scripts/fig_dig.png')

    
    ##################################
    ### Procesamiento de la imagen ###
    ##################################

    # 1.Conversion de la imagen a Escala de Grises
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

    # 2.Se filtra la imagen en escala de grises con el filtro GaussianBlur
    blur = cv2.GaussianBlur(gray,(3,3),0)
    
    # 3.Utilizando la imagen en escala de grises se binariza utilizando el motodo canny
    #   dejando unicamente en blanco los contornos
    canny = cv2.Canny(blur, 50,150)
    
    # 4.Con las siguientes dos lineas de codigo se busca cerrar los contronos los mejor posible
    kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
    closed=cv2.morphologyEx(canny,cv2.MORPH_CLOSE,kernel,iterations=2)

    # 5.Se buscan los contornos existentes en la imagen filtrada
    _,cnts,_ = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #OpenCV 3

    # 6.Se crea una lista para guardar los contornos que cumplan las condiciones de area
    ncnts = []

    # 7.Se evaluan todos los contornos si tienen un area mayor a 1900 y de acuerdo a esto
    #   se guarda en la lista y de dibuja el contorno en verde.
    for c in cnts:
      area = cv2.contourArea(c)
      if area > 1900:
        # Se comprueba la curva si tiene defectos de convexidad y la corrige con el metodo convexhull.
        nuevoContorno = cv2.convexHull(c)
        cv2.drawContours(cv_image, [nuevoContorno], -1,(0,255,0), 3,cv2.LINE_AA)
        ncnts.append(nuevoContorno)


    # 7.Se transforma la imagen al formato HSV
    imageHSV = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

    # 8.Se analizan todos los contornos y se determina color y forma de la figura correspondiente
    for c in ncnts:
      # se crea un rectangulo delimitador que no considera. Lo que permite hallar 
      # (x, y) la coordenada superior izquierda del rectangulo y  (w, h) su anchura y altura.
      x, y, w, h = cv2.boundingRect(c)

      # se crea una imagen auxiliar solo para dibujar los contronos independientes
      imAux = np.zeros(cv_image.shape[:2], dtype="uint8")
      imAux = cv2.drawContours(imAux, [c], -1, 255, -1)
      maskHSV = cv2.bitwise_and(imageHSV,imageHSV, mask=imAux)
      
      # Se determina nombre y color de la figura
      name = figName(c,w,h)
      color1 = figColor(maskHSV)

      # Dibujamos el texto en la imagen original
      nameColor = name + " " + color1
      cv2.putText(cv_image,nameColor,(x,y-5),1,0.8,(0,255,0),1)
   
    #########################################
    ### Fin del procesamienro de imagenes ###
    #########################################

    # Se crean ventanas para mostrar las imagenes original y procesada. si desea ver las otras
    # ventanas descomente los otros cv2.imshow()
    cv2.imshow(SHOW_WINDOW, cv_image)
    cv2.imshow(FILTERED_WINDOWS[0], canny)
    #cv2.imshow(FILTERED_WINDOWS[1], imageHSV)

    cv2.waitKey(3)

    # Se envia la imagen procesada mediante el topic
    try:
      self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
    except CvBridgeError as e:
      print(e)

  # Metodo destructor para cerrar las ventanas abiertas
  def __del__(self):
    cv2.destroyAllWindows()


def main(args):
  
  # Se crea el objeto
  ic = image_converter()

  # Se inicializa el nodo de ROS
  rospy.init_node(NODE_NAME, anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  
# Funcion principal
if __name__ == '__main__':
    main(sys.argv)



