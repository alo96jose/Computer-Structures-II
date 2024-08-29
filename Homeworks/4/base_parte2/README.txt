---------------- Tarea 4:  Simulador de Memoria Caché ------------------
---- Instrucciones y consideraciones para la ejecución del programa ----
----------------------------- Parte 2 ----------------------------------

#-----------------------------------------------------------------------#

* Generales:
1. Para poder ejecutar de forma correcta las simulaciones, se recomienda abrir la terminal (CMD) en Windows.
2. También, es importante asegurarse de que el path en terminal, corresponda con el directorio donde se encuentra el proyecto (carpeta llamada: base_parte2).

* Caso del Caché de un único nivel (similar al comando de la parte 1):
1. Ejecutar el programa en terminal, siguiendo la sintáxis del comando:

python cache_sim.py --l1_s 32 --l1_a 8 -b 64 -t ./traces/traces/400.perlbench-41B.trace.txt.gz

* Caso del Caché con dos niveles (habilitar L2 con "--l2" y agregar parámetros):
1. Ejecutar el programa en terminal, siguiendo la sintáxis del comando:

python cache_sim.py --l1_s 32 --l1_a 8 --l2 --l2_s 64 --l2_a 8 -b 64 -t ./traces/traces/400.perlbench-41B.trace.txt.gz 

* Caso del Caché con Presencia de L3 (habilitar L3 con "--l3" y agregar parámetros):
1. Ejecutar el programa en terminal, siguiendo la sintáxis del comando:

python cache_sim.py --l1_s 32 --l1_a 8 --l2 --l2_s 256 --l2_a 8 --l3 --l3_s 512 --l3_a 16 -b 64 -t ./traces/traces/400.perlbench-41B.trace.txt.gz



#----#--#----#
# Importante #
#----#--#----#

* Lo anterior es para una recopilación de resultados uno a uno. Para efectos del desarrollo de la tarea, estos se recopilaron corriendo bash scripts para las distintas partes del enunciado.
* La política LRU está configurada por default (no es necesario especificarla en el comando).


*--------------------*--------------------*
Estudiantes:

José Alejandro Castillo Sequeira
Sharlin Hernández Sánchez
Alonso Jiménez Anchía