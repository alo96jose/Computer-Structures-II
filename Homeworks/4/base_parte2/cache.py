from math import log2   # Importa la función log2 desde el módulo math
from random import randint   # Importa la función randint desde el módulo random
from pdb import set_trace   # Importa la función set_trace desde el módulo pdb

class Cache:
    """
    Representa una caché con capacidades y políticas específicas.

    Parámetros:
    - capacity_kb (int): Capacidad de la caché en kilobytes.
    - associativity (int): Asociatividad de la caché.
    - block_size_bytes (int): Tamaño del bloque en bytes.
    - replacement_policy (str): Política de reemplazo ('l' para LRU, 'r' para aleatorio).
    - level (int): Nivel de la caché.

    Atributos públicos:
    - total_accesses (int): Contador de accesos totales.
    - total_misses (int): Contador de fallos totales.
    """

    def __init__(self, capacity_kb, associativity, block_size_bytes, replacement_policy, level):
        """
        Inicializa una instancia de Cache con los parámetros especificados.
        """
        self.total_accesses = 0   # Inicializa el contador de accesos totales
        self.total_misses = 0   # Inicializa el contador de fallos totales

        # Inicializa los parámetros de la caché
        self._init_cache_params(capacity_kb, associativity, block_size_bytes)
        self.replacement_policy = replacement_policy   # Asigna la política de reemplazo
        self.level = level   # Asigna el nivel de la caché

        # Inicializa las estructuras de la caché
        self._init_cache_structures()

    def _init_cache_params(self, capacity_kb, associativity, block_size_bytes):
        """
        Inicializa los parámetros de configuración de la caché.
        
        Parámetros:
        - capacity_kb (int): Capacidad de la caché en kilobytes.
        - associativity (int): Asociatividad de la caché.
        - block_size_bytes (int): Tamaño del bloque en bytes.
        """
        self.capacity_kb = int(capacity_kb)   # Capacidad de la caché en kilobytes
        self.associativity = int(associativity)   # Asociatividad de la caché
        self.block_size_bytes = int(block_size_bytes)   # Tamaño del bloque en bytes

        # Calcula los bits de desplazamiento de byte, conjuntos y etiqueta
        self.byte_offset_bits = int(log2(self.block_size_bytes))
        self.num_sets = int((self.capacity_kb * 1024) / (self.block_size_bytes * self.associativity))
        self.index_bits = int(log2(self.num_sets))
        self.tag_bits = int(log2(self.associativity))

    def _init_cache_structures(self):
        """
        Inicializa las estructuras de datos internas de la caché.
        """
        # Inicializa matrices para los bits válidos, etiquetas y edades de cada conjunto
        self.valid_bits = [[False] * self.associativity for _ in range(self.num_sets)]
        self.tags = [[0] * self.associativity for _ in range(self.num_sets)]
        self.ages = [[0] * self.associativity for _ in range(self.num_sets)]

    def display_stats(self):
        """
        Muestra estadísticas de fallos de la caché en formato de cadena.

        Retorna:
        - stats_str (str): Cadena formateada con estadísticas de fallos.
        """
        # Calcula la tasa de fallos y la convierte en cadena con formato
        miss_rate = (100.0 * self.total_misses) / self.total_accesses
        miss_rate_str = f"{miss_rate:.3f}%"
        stats_str = f"Total Misses: {self.total_misses}, Miss Rate: {miss_rate_str}"
        return stats_str

    def calculate_indices(self, access_type, address):
        """
        Calcula el índice de conjunto y la etiqueta para una dirección de acceso.

        Parámetros:
        - access_type (str): Tipo de acceso ('read' o 'write').
        - address (int): Dirección de memoria a acceder.

        Retorna:
        - set_index (int): Índice de conjunto calculado.
        - tag (int): Etiqueta calculada.
        """
        set_index = (address // (2 ** self.byte_offset_bits)) % (2 ** self.index_bits)
        tag = address // (2 ** (self.byte_offset_bits + self.index_bits))
        return set_index, tag

    def simulate_access(self, access_type, address):
        """
        Simula un acceso a la caché, determinando si es un acierto o fallo.

        Parámetros:
        - access_type (str): Tipo de acceso ('read' o 'write').
        - address (int): Dirección de memoria a acceder.

        Retorna:
        - access_hit (bool): True si el acceso fue un acierto, False si fue un fallo.
        """
        set_index, tag = self.calculate_indices(access_type, address)
        data_found = any(self.valid_bits[set_index][i] and self.tags[set_index][i] == tag for i in range(self.associativity))
        access_hit = data_found   # Determina si el acceso fue un acierto
        self.ages[set_index] = [max(self.ages[set_index]) + 1 if self.valid_bits[set_index][i] and self.tags[set_index][i] == tag else age
                                for i, age in enumerate(self.ages[set_index])]
        self.total_accesses += 1   # Incrementa el contador de accesos totales
        return access_hit

    def load_to_cache(self, set_index, tag):
        """
        Carga un bloque a la caché y maneja un fallo.

        Parámetros:
        - set_index (int): Índice de conjunto donde se cargará el bloque.
        - tag (int): Etiqueta del bloque.

        """
        self.total_misses += 1   # Incrementa el contador de fallos totales
        replace_function = self._replace_least_recently_used if self.replacement_policy == "l" else self._replace_random
        # Llama a la función de reemplazo elegida
        replace_function(set_index, tag)

    def _replace_least_recently_used(self, set_index, tag):
        """
        Reemplaza el elemento menos recientemente usado en la caché.

        Parámetros:
        - set_index (int): Índice de conjunto donde se realizará el reemplazo.
        - tag (int): Etiqueta del bloque a reemplazar.
        """
        victim_index = self.ages[set_index].index(min(self.ages[set_index]))

        self.valid_bits[set_index][victim_index] = True
        self.tags[set_index][victim_index] = tag
        self.ages[set_index][victim_index] = max(self.ages[set_index])

        # Actualiza las edades (excluyendo el víctima) usando comprensión de lista
        self.ages[set_index] = [age - 1 if i != victim_index else age
                                for i, age in enumerate(self.ages[set_index])]

    def _replace_random(self, set_index, tag):
        """
        Reemplaza aleatoriamente un elemento en la caché.

        Parámetros:
        - set_index (int): Índice de conjunto donde se realizará el reemplazo.
        - tag (int): Etiqueta del bloque a reemplazar.
        """
        victim_index = randint(0, self.associativity - 1)
        self.valid_bits[set_index][victim_index] = True
        self.tags[set_index][victim_index] = tag


