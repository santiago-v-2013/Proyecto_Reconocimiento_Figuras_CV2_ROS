# Proyecto_Reconocimiento_Figuras_CV2_ROS

Este proyecto tiene como fin que mediante una camara se pueda realizar el reconocimiento de figuras como circulos, cuadrados, hexagonos, pentagonos, restangulos y trinagulos haciendo uso de la librería OpenCv en ROS, debido a que esta facilita las etapas de filtrado y procesamiento de la imagen para llegar al reconocimiento final.

![Imagen 1: Reconocimiento de figuras y colores](https://github.com/santiago-v-2013/Proyecto_Reconocimiento_Figuras_CV2_ROS/blob/main/Imagenes/resultado.png)

En la imagen anterior se puede observar el resultado. Apesar de las etapas de procesamiento se puede ver que hay un error en el reconocimiento del color azul, esto es cuestios de ajustar mejor los limites dentro del esquema de reconocimiento de color mediante el esquema HSV.

## 1) Crear workspace de catkin

Para crear el workspace en un terminal se ejecuta la siguientes sentencia

```
mkdir -p ~/catkin_ws/src
```

Posteriormente debemos construir el directorio para esto debemos entrar al mismo y luego realizar las construccion

```
cd ~/catkin_ws/  # Se accede al directorio
catkin_make      # Se construye el directorio
```

Finalmente para que quede listo el directorio debemos agregarlo al bash

```
sudo gedit .bashrc
```

## 2) Instalar la carpeta proyecto

Para esto se debe clonar el directorio dentro de la carpetar src.

* Se accede a la carpeta src dentro del workspace

```
cd ~/catkin_ws/src
```

* Se clona el directorio dentro de la carpeta


```
git clone https://github.com/santiago-v-2013/Proyecto_Reconocimiento_Figuras_CV2_ROS.git

```

## 3) Ejecutar el launch

* Se inicializa el roscore en un primer terminal

```
roscore
```

* Se ejecuta el launch que contiene la configuracion de la camara y de los nodos necesarios
```
roslaunch proyecto identificar.launch
```

## Autores

* Santiago Vasquez 


