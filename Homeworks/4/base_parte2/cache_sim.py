from optparse import OptionParser   # Importa OptionParser para procesar opciones de línea de comandos.
import gzip   # Importa gzip para manejar archivos comprimidos gzip.
import sys   # Importa sys para acceso a variables y funciones relacionadas con el sistema.
from cache import Cache   # Importa la clase Cache desde el módulo cache.
from pdb import set_trace   # Importa set_trace desde pdb para depuración interactiva.

# Parsing command-line options
option_parser = OptionParser()   # Crea un objeto OptionParser para manejar opciones de línea de comandos.
option_parser.add_option("--l1_s", dest="l1_size")   # Define una opción --l1_s para el tamaño de la L1 cache.
option_parser.add_option("--l1_a", dest="l1_assoc")   # Define una opción --l1_a para la asociatividad de la L1 cache.
option_parser.add_option("--l2", action="store_true", dest="include_l2")   # Define una opción --l2 para incluir la L2 cache.
option_parser.add_option("--l2_s", dest="l2_size")   # Define una opción --l2_s para el tamaño de la L2 cache.
option_parser.add_option("--l2_a", dest="l2_assoc")   # Define una opción --l2_a para la asociatividad de la L2 cache.
option_parser.add_option("--l3", action="store_true", dest="include_l3")   # Define una opción --l3 para incluir la L3 cache.
option_parser.add_option("--l3_s", dest="l3_size")   # Define una opción --l3_s para el tamaño de la L3 cache.
option_parser.add_option("--l3_a", dest="l3_assoc")   # Define una opción --l3_a para la asociatividad de la L3 cache.
option_parser.add_option("-b", dest="block_size", default="64")   # Define una opción -b para el tamaño del bloque por defecto a 64 bytes.
option_parser.add_option("-t", dest="trace_file")   # Define una opción -t para el archivo de traza.

(options, args) = option_parser.parse_args()   # Parsea los argumentos de la línea de comandos y los guarda en options y args.

# Print input configuration parameters
print("Input Configuration Parameters:")   # Imprime la cabecera de configuración de parámetros de entrada.
print(f"L1 Size: {options.l1_size} kB")   # Imprime el tamaño de la L1 cache.
print(f"L1 Associativity: {options.l1_assoc}")   # Imprime la asociatividad de la L1 cache.
print(f"L2 Present: {options.include_l2}")   # Imprime si está presente la L2 cache.
print(f"L2 Size: {options.l2_size} kB") if options.include_l2 else None   # Imprime el tamaño de la L2 cache si está presente.
print(f"L2 Associativity: {options.l2_assoc}") if options.include_l2 else None   # Imprime la asociatividad de la L2 cache si está presente.
print(f"L3 Present: {options.include_l3}")   # Imprime si está presente la L3 cache.
print(f"L3 Size: {options.l3_size} kB") if options.include_l3 else None   # Imprime el tamaño de la L3 cache si está presente.
print(f"L3 Associativity: {options.l3_assoc}") if options.include_l3 else None   # Imprime la asociatividad de la L3 cache si está presente.
print(f"Block Size: {options.block_size} B")   # Imprime el tamaño del bloque.
print(f"Trace File: {options.trace_file}")   # Imprime el nombre del archivo de traza.
print()

cache_hierarchy = []   # Inicializa una lista para almacenar la jerarquía de cachés.

# Crea la L1 cache y la añade a cache_hierarchy.
l1_cache = Cache(options.l1_size, options.l1_assoc, options.block_size, "l", 1)
cache_hierarchy.append(l1_cache)

# Crea la L2 cache y la añade a cache_hierarchy si está incluida (--l2).
l2_cache = Cache(options.l2_size, options.l2_assoc, options.block_size, "l", 2) if options.include_l2 else None
if l2_cache:
    cache_hierarchy.append(l2_cache)

# Crea la L3 cache y la añade a cache_hierarchy si está incluida (--l3) y también está incluida la L2 cache.
l3_cache = Cache(options.l3_size, options.l3_assoc, options.block_size, "l", 3) if options.include_l3 and options.include_l2 else None
if l3_cache:
    cache_hierarchy.append(l3_cache)

# Process the trace file
with gzip.open(options.trace_file, 'rt') as trace:
    for entry in trace:
        entry = entry.rstrip()   # Elimina los espacios en blanco al final de la entrada.
        access_type, hex_address = entry.split(" ")   # Divide la entrada en tipo de acceso y dirección hexadecimal.
        address = int(hex_address, 16)   # Convierte la dirección hexadecimal en entero.

        # Simulate access for each cache in cache_hierarchy
        access_results = [cache.simulate_access(access_type, address) for cache in cache_hierarchy]

        # Load to cache or break on first cache miss
        [cache_hierarchy[i].load_to_cache(*cache_hierarchy[i].calculate_indices(access_type, address))
         if not hit else None for i, hit in enumerate(access_results)]

# Create a list of simulation results for each cache level
simulation_results = [
    f"L1 Cache: {l1_cache.display_stats()}",
    f"L2 Cache: {l2_cache.display_stats()}" if options.include_l2 else "",   # Añade estadísticas de la L2 cache si está presente.
    f"L3 Cache: {l3_cache.display_stats()}" if options.include_l3 else ""   # Añade estadísticas de la L3 cache si está presente.
]

trace_filename = str(options.trace_file).replace("../../traces/", "")   # Obtiene el nombre del archivo de traza.
simulation_results.insert(0, trace_filename)   # Inserta el nombre del archivo de traza al principio de la lista.
results_str = '\n'.join(simulation_results)   # Convierte la lista de resultados en una sola cadena separada por líneas.
print()
print(results_str)   # Imprime los resultados de la simulación.
