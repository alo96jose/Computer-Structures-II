from optparse import OptionParser
import gzip
from cache import Cache  # Importar la clase Cache desde el módulo cache

# Configurar el parser de opciones
parser = OptionParser()
parser.add_option("-s", dest="cache_capacity")  # Capacidad de la caché
parser.add_option("-a", dest="cache_assoc")  # Asociatividad de la caché
parser.add_option("-b", dest="block_size")  # Tamaño del bloque
parser.add_option("-r", dest="repl_policy")  # Política de reemplazo
parser.add_option("-t", dest="TRACE_FILE")  # Archivo de traza

# Parsear los argumentos de la línea de comandos
(options, args) = parser.parse_args()

# Crear una instancia de la clase Cache con los parámetros proporcionados
cache = Cache(options.cache_capacity, options.cache_assoc, options.block_size, options.repl_policy)

# Variables para debug (pueden ser eliminadas en producción)
i = 0

# Abrir el archivo de traza comprimido con gzip y leer línea por línea
with gzip.open(options.TRACE_FILE, 'rt') as trace_fh:
    for line in trace_fh:
        line = line.rstrip()  # Eliminar caracteres de nueva línea o espacios en blanco al final
        access_type, hex_str_address = line.split(" ")  # Separar el tipo de acceso y la dirección en formato hexadecimal
        address = int(hex_str_address, 16)  # Convertir la dirección de hexadecimal a entero
        cache.acceso(access_type, address)  # Realizar el acceso a la caché según el tipo y la dirección

        # Debug: limitar el número de iteraciones (eliminar en producción)
        # i += 1
        # if i == 25:
        #     break

# Imprimir información y estadísticas de la caché
# cache.imprimir_info()
cache.imprimir_estadisticas()


