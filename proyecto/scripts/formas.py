#!/usr/bin/env python

# Librerias

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
NODE_NAME = "formas"

SHOW_WINDOW = "Imagen resultado"
FILTERED_WINDOWS = ["Imagen filtrada_1","Imagen filtrada_2"]

TOPIC_SUB_IMAGE_IN = "image_input"
TOPIC_PUB_IMAGE_OUT = "imagen_output"


def figColor(imagenHSV):
  # Rojo
  rojoBajo1 = np.array([0, 100, 20], np.uint8)
  rojoAlto1 = np.array([10, 255, 255], np.uint8)
  rojoBajo2 = np.array([175, 100, 20], np.uint8)
  rojoAlto2 = np.array([180, 255, 255], np.uint8)

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

  # se buscan los colores en la imagen, segun los limites altos 
  # y bajos dados
  maskRojo1 = cv2.inRange(imagenHSV, rojoBajo1, rojoAlto1)
  maskRojo2 = cv2.inRange(imagenHSV, rojoBajo2, rojoAlto2)
  maskRojo = cv2.add(maskRojo1, maskRojo2)
  maskNaranja = cv2.inRange(imagenHSV, naranjaBajo, naranjaAlto)
  maskAmarillo = cv2.inRange(imagenHSV, amarilloBajo, amarilloAlto)
  maskVerde = cv2.inRange(imagenHSV, verdeBajo, verdeAlto)
  maskVioleta = cv2.inRange(imagenHSV, violetaBajo, violetaAlto)
  maskRosa = cv2.inRange(imagenHSV, rosaBajo, rosaAlto)
	
  cntsRojo = cv2.findContours(maskRojo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0] #Reemplaza por 1, si tienes OpenCV3	
  cntsNaranja = cv2.findContours(maskNaranja, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0] #Reemplaza por 1, si tienes OpenCV3
  cntsAmarillo = cv2.findContours(maskAmarillo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0] #Reemplaza por 1, si tienes OpenCV3
  cntsVerde = cv2.findContours(maskVerde, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0] #Reemplaza por 1, si tienes OpenCV3
  cntsVioleta = cv2.findContours(maskVioleta, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0] #Reemplaza por 1, si tienes OpenCV3
  cntsRosa = cv2.findContours(maskRosa, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0] #Reemplaza por 1, si tienes OpenCV3

  if len(cntsRojo)>0: color = 'Rojo'
  elif len(cntsNaranja)>0: color = 'Naranja'
  elif len(cntsAmarillo)>0: color = 'Amarillo'
  elif len(cntsVerde)>0: color = 'Verde'
  elif len(cntsVioleta)>0: color = 'Violeta'
  elif len(cntsRosa)>0: color = 'Rosa'

  return color
		
def figName(contorno,width,height):
  global namefig
  epsilon = 0.01*cv2.arcLength(contorno,True)
  approx = cv2.approxPolyDP(contorno,epsilon,True)

  if len(approx) == 3:
    namefig = 'Triangulo'

  if len(approx) == 4:
    aspect_ratio = float(width)/height
    if aspect_ratio == 1:
      namefig = 'Cuadrado'
    else:
      namefig = 'Rectangulo'

  if len(approx) == 5:
    namefig = 'Pentagono'

  if len(approx) == 6:
    namefig = 'Hexagono'

  if len(approx) > 10:
    namefig = 'Circulo'

  return namefig

# Definicion de la clase
class image_converter:

  def __init__(self):
  
    self.image_pub = rospy.Publisher(TOPIC_PUB_IMAGE_OUT,Image)
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber(TOPIC_SUB_IMAGE_IN,Image,self.callback)

  def callback(self,data):
    global namefig
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)

    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(gray, 10,150)
    canny = cv2.dilate(canny,None,iterations=1)
    canny = cv2.erode(canny,None,iterations=1)

    _,cnts,_ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #OpenCV 3
    imageHSV = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)


    for c in cnts:
      x, y, w, h = cv2.boundingRect(c)
      imAux = np.zeros(cv_image.shape[:2], dtype="uint8")
      imAux = cv2.drawContours(imAux, [c], -1, 255, -1)
      maskHSV = cv2.bitwise_and(imageHSV,imageHSV, mask=imAux)
      name = figName(c,w,h)
      color = figColor(maskHSV)
      nameColor = name + ' ' + color
      cv2.putText(cv_image,nameColor,(x,y-5),1,0.8,(0,255,0),1)

    cv2.imshow(SHOW_WINDOW, cv_image)
    #cv2.imshow(FILTERED_WINDOWS[0], canny)
    #cv2.imshow(FILTERED_WINDOWS[1], imageHSV)
    cv2.waitKey(3)

    try:
      self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
    except CvBridgeError as e:
      print(e)

def main(args):
  ic = image_converter()
  rospy.init_node(NODE_NAME, anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
