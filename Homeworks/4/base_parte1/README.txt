---------------- Tarea 4:  Simulador de Memoria Caché ------------------
---- Instrucciones y consideraciones para la ejecución del programa ----
----------------------------- Parte 1 ----------------------------------

#-----------------------------------------------------------------------#

* Generales:
1. Para poder ejecutar de forma correcta las simulaciones, se recomienda abrir la terminal (CMD) en Windows.
2. También, es importante asegurarse de que el path en terminal, corresponda con el directorio donde se encuentra el proyecto (carpeta llamada: base_parte1).

* Caso del Efecto del tamaño del caché (variar parámetro "s" en el comando):
1. Ejecutar el programa en terminal, siguiendo la sintáxis del comando:

python cache_sim.py -s 128 -a 16 -b 64 -r LRU -t ./traces/traces/403.gcc-16B.trace.txt.gz

* Caso del Efecto de la asociatividad del caché (variar parámetro "a" en el comando):
1. Ejecutar el programa en terminal, siguiendo la sintáxis del comando:

python cache_sim.py -s 128 -a 16 -b 64 -r LRU -t ./traces/traces/403.gcc-16B.trace.txt.gz 

* Caso del Efecto del tamaño del bloque en el caché (variar parámetro "b" en el comando):
1. Ejecutar el programa en terminal, siguiendo la sintáxis del comando:

python cache_sim.py -s 128 -a 16 -b 64 -r LRU -t ./traces/traces/403.gcc-16B.trace.txt.gz

* Caso del Efecto de la política de reemplazo del caché (variar parámetro "r", entre: "LRU" y "r" en el comando):
1. Ejecutar el programa en terminal, siguiendo la sintáxis del comando:

python cache_sim.py -s 128 -a 16 -b 64 -r r -t ./traces/traces/403.gcc-16B.trace.txt.gz


#----#--#----#
# Importante #
#----#--#----#

* Lo anterior es para una recopilación de resultados uno a uno. Para efectos del desarrollo de la tarea, estos se recopilaron corriendo bash scripts para las distintas partes del enunciado.


*--------------------*--------------------*
Estudiantes:

José Alejandro Castillo Sequeira
Sharlin Hernández Sánchez
Alonso Jiménez Anchía