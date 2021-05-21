# Proyecto_Reconocimiento_Figuras_CV2_ROS
Este proyecto realiza un reconocimiento de figuras y sus colores utilizando la librería de OpenCv en ROS

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

## Agradecimientos

Parte del codigo de "figuras.py" fue extraido del codigo del canal de youtube Omes.

Link: https://www.youtube.com/channel/UCCDvMED1sysAbF5qOfmEw3A

## Autores

* Santiago Vasquez 


