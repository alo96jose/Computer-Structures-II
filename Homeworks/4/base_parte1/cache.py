from math import log2, floor

class Cache:
    def __init__(self, capacidad_cache, asociatividad_cache, tamano_bloque, politica_reemplazo):
        """
        Inicializa una instancia de Cache con los parámetros dados.

        Parámetros:
        capacidad_cache (int): Capacidad de la caché en kilobytes.
        asociatividad_cache (int): Número de vías o conjunto asociativo.
        tamano_bloque (int): Tamaño de bloque en bytes.
        politica_reemplazo (str): Política de reemplazo ('lru' o 'otra').

        Salida:
        None
        """
        self.total_accesos = 0
        self.total_fallos = 0
        self.capacidad_cache = int(capacidad_cache)
        self.asociatividad_cache = int(asociatividad_cache)
        self.tamano_bloque = int(tamano_bloque)
        self.politica_reemplazo = politica_reemplazo.lower()
        self.byte_offset_size = int(log2(self.tamano_bloque))
        self.num_sets = int((self.capacidad_cache * 1024) / (self.tamano_bloque * self.asociatividad_cache))
        self.index_size = int(log2(self.num_sets))
        self.tabla_valida = [[False for _ in range(self.asociatividad_cache)] for _ in range(self.num_sets)]
        self.tabla_etiquetas = [[0 for _ in range(self.asociatividad_cache)] for _ in range(self.num_sets)]
        self.tabla_reemplazo = [[0 for _ in range(self.asociatividad_cache)] for _ in range(self.num_sets)]

    def imprimir_info(self):
        """
        Imprime los parámetros de la caché.

        Parámetros:
        None

        Salida:
        None
        """
        print("Parámetros del caché:")
        print("\tCapacidad:\t\t\t" + str(self.capacidad_cache) + "kB")
        print("\tAssociatividad:\t\t\t" + str(self.asociatividad_cache))
        print("\tTamaño de Bloque:\t\t" + str(self.tamano_bloque) + "B")
        print("\tPolítica de Reemplazo:\t\t" + str(self.politica_reemplazo))

    def imprimir_estadisticas(self):
        """
        Imprime las estadísticas de fallos de la caché.

        Parámetros:
        None

        Salida:
        None
        """
        porcentaje_fallos = (100.0 * self.total_fallos) / self.total_accesos
        porcentaje_fallos = "{:.3f}".format(porcentaje_fallos)

        print(f"Cantidad total de misses: {self.total_fallos}, Miss rate total: {porcentaje_fallos}%")

    def acceso(self, tipo_acceso, direccion):
        """
        Simula el acceso a la caché y actualiza las estadísticas.

        Parámetros:
        tipo_acceso (str): Tipo de acceso ('lectura' o 'escritura').
        direccion (int): Dirección de memoria accedida.

        Salida:
        bool: True si hubo un fallo de caché (miss), False si hubo un acierto (hit).
        """
        byte_offset = direccion % (2 ** self.byte_offset_size)
        index = (direccion // (2 ** self.byte_offset_size)) % (2 ** self.index_size)
        etiqueta = direccion // (2 ** (self.byte_offset_size + self.index_size))

        hit = self.buscar(index, etiqueta)

        if hit == -1:
            self.traer_a_cache(index, etiqueta)
            self.total_fallos += 1

        self.total_accesos += 1

        return hit == -1

    def buscar(self, index, etiqueta):
        """
        Busca si un bloque está en la caché.

        Parámetros:
        index (int): Índice del conjunto.
        etiqueta (int): Etiqueta del bloque.

        Salida:
        int: Índice de la vía si hay hit, -1 si no se encontró el bloque en la caché.
        """
        for i in range(self.asociatividad_cache):
            if self.tabla_valida[index][i] and self.tabla_etiquetas[index][i] == etiqueta:
                if self.politica_reemplazo == "lru":
                    self.tabla_reemplazo[index][i] = self.asociatividad_cache - 1
                    for j in range(self.asociatividad_cache):
                        if j != i:
                            self.tabla_reemplazo[index][j] -= 1
                return i
        return -1

    def traer_a_cache(self, index, etiqueta):
        """
        Trae un bloque a la caché, aplicando la política de reemplazo si es necesario.

        Parámetros:
        index (int): Índice del conjunto.
        etiqueta (int): Etiqueta del bloque.

        Salida:
        None
        """
        for i in range(self.asociatividad_cache):
            if not self.tabla_valida[index][i]:
                self.tabla_valida[index][i] = True
                self.tabla_etiquetas[index][i] = etiqueta
                self.tabla_reemplazo[index][i] = self.asociatividad_cache - 1
                for j in range(self.asociatividad_cache):
                    if j != i:
                        self.tabla_reemplazo[index][j] -= 1
                return

        if self.politica_reemplazo == "lru":
            posicion_LRU = min(range(self.asociatividad_cache), key=lambda x: self.tabla_reemplazo[index][x])
            self.tabla_etiquetas[index][posicion_LRU] = etiqueta
            self.tabla_reemplazo[index][posicion_LRU] = self.asociatividad_cache - 1
            for i in range(self.asociatividad_cache):
                if i != posicion_LRU:
                    self.tabla_reemplazo[index][i] -= 1
