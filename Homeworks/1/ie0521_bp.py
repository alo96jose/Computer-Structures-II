import math

class ie0521_bp:
    """
    Definiendo los parametros a utilizar en el predictor Hibrido GShared/Perceptron llamado Lonnis
    # gshare_size: Tamano de entradas para el GShare
    # perceptron_count: Numero de Perceptrones a usar
    # history_size: Tamano de global history branch SR o tamanno de los Pesos del perceptron

    # Presupuesto Limite = 32768 bits = 2^15 bits

    2^9 = 512
    2^10 = 1024
    2^ 11 = 2048
    2^12 = 4096

    """

    def __init__(self, gshare_size=5120, perceptron_count=80, history_size=32):
        # Inicializando  gshare predictor
        self.gshare_table = [0] * gshare_size  # 2-bit cter inicializados en  '00'
        self.global_history = 0  # Global history register

        # Inicializando perceptron 
        self.perceptrons = [[0] * (history_size + 1) for _ in range(perceptron_count)]
        self.history_size = history_size
        # self.threshold = int(1.93 * history_size + 14)
        self.threshold = math.floor(1.93 * history_size + 14)
        
        

        # Inicializando selector
        #self.selector = [0] * self.selector_size  # 2-bit saturating cters inicializados en  '00'  # nouv
        # self.selector = [0] * gshare_size  # 2-bit saturating cters inicializados en  '00'

        # Inicializando selector con un tamaño de (gshare size // (2^8 = 256)
        self.selector = [0] * (gshare_size // 256)  # 2-bit saturating counters initialized to '00'
        
        # self.selector = [0] * gshare_size  # 2-bit saturating counters initialized to '00'

        # Stats
        self.total_predictions = 0
        self.total_taken_pred_taken = 0
        self.total_taken_pred_not_taken = 0
        self.total_not_taken_pred_taken = 0
        self.total_not_taken_pred_not_taken = 0


    def print_info(self):
        print("Parámetros del predictor:")
        print("\tTipo de predictor:\t\t\tLonnis")
        print("\tNúmero de entradas de GShare:\t\t", len(self.gshare_table))
        print("\tNúmero de Perceptrones:\t\t\t", len(self.perceptrons))
        print("\tTamaño del Historial Global:\t\t", self.history_size)
        print("\tNúmero de entradas de Selector:\t\t", (len(self.gshare_table) // 256))
        print("\tPresupuesto Estimado: \t\t\t", ( (len(self.perceptrons)*(self.history_size + 1)*8) + (len(self.gshare_table) + len(self.selector ) )*2 ))
        print("\tEcuacion Presupuesto: (NumPercep * w_i (HistGloR +1 ) * 8 )+ (InputsGshareSize*2 + SelectorSize*2)")
        # Presupuesto Limite = 32768 bits

    def print_stats(self):
        print("Resultados de la simulación")
        print("\t# branches:\t\t\t\t\t\t" + str(self.total_predictions))
        print("\t# branches tomados predichos correctamente:\t\t" + str(self.total_taken_pred_taken))
        print("\t# branches tomados predichos incorrectamente:\t\t" + str(self.total_taken_pred_not_taken))
        print("\t# branches no tomados predichos correctamente:\t\t" + str(self.total_not_taken_pred_not_taken))
        print("\t# branches no tomados predichos incorrectamente:\t" + str(self.total_not_taken_pred_taken))
        perc_correct = 100 * (self.total_taken_pred_taken + self.total_not_taken_pred_not_taken) / self.total_predictions
        formatted_perc = "{:.3f}".format(perc_correct)
        print("\t% predicciones correctas:\t\t\t\t" + str(formatted_perc) + "%")

    def predict(self, PC):
        # Predice con GShare
        gshare_index = int(PC) % len(self.gshare_table)
        gshare_prediction = 'T' if self.gshare_table[gshare_index] >= 2 else 'N'

        
        # Predice con Perceptron
        perceptron_index = int(PC) % len(self.perceptrons)
        weights = self.perceptrons[perceptron_index]
        y = weights[0]  # bias weight
        for i in range(1, self.history_size + 1):
            y += weights[i] * (1 if (self.global_history & (1 << (i - 1))) else -1)
        # perceptron_prediction = "T" if y >= 0 else "N"
        if y >= 0:
            perceptron_prediction = "T"
        else:
            perceptron_prediction = "N"

        # Mapea gshare index al selector index que es menor
        selector_index = gshare_index % len(self.selector)

        # Usa selector para escoger la mejor prediccion
        if self.selector[selector_index] > 1:
        # if self.selector[gshare_index] > 1:
            final_prediction = gshare_prediction
        else:
            final_prediction = perceptron_prediction

        return final_prediction

        # # Inviertiendo el Contador de Selector
        # # Usa selector para escoger la mejor prediccion
        # if self.selector[gshare_index] > 1:
        #     final_prediction = gshare_prediction
        # else:
        #     final_prediction = perceptron_prediction

        # return final_prediction

    def update(self, PC, result, prediction):

        gshare_index = int(PC) % len(self.gshare_table)
        perceptron_index = int(PC) % len(self.perceptrons)
        weights = self.perceptrons[perceptron_index]
        selector_index = gshare_index % len(self.selector)

        # Update GShare
        if result == 'T':
            if self.gshare_table[gshare_index] < 3:
                self.gshare_table[gshare_index] += 1
        else:
            if self.gshare_table[gshare_index] > 0:
                self.gshare_table[gshare_index] -= 1

        # Update Perceptron
        result_value = 1 if result == "T" else -1
        for i in range(1, self.history_size + 1):
            weights[i] += result_value * (1 if (self.global_history & (1 << (i - 1))) else -1)
            # Para limitar los Pesos a 8 bits segun lo mencionado en el Paper
            weights[i] = max(-128, min(127, weights[i]))
        weights[0] += result_value  # Update bias weight

        # Para limitar los Pesos a 8 bits segun lo mencionado en el Paper
        weights[0] = max(-128, min(127, weights[0]))

        # Update global history
        self.global_history = ((self.global_history << 1) | (1 if result == "T" else 0)) & ((1 << self.history_size) - 1)
        # self.global_history = ((self.global_history << 1) or (1 if result == "T" else 0)) and ((1 << self.history_size) - 1)

        # Update selector basado en la confiabilidad de la prediccion 
        correct_prediction = (prediction == result)
        if correct_prediction:
            if self.selector[selector_index] < 3:
                self.selector[selector_index] += 1
        else:
            if self.selector[selector_index] > 0:
                self.selector[selector_index] -= 1

        # Update stats
        
        if result == "T" and prediction == "T":
            self.total_taken_pred_taken += 1
        elif result == "T" and prediction == "N":
            self.total_taken_pred_not_taken += 1
        elif result == "N" and prediction == "N":
            self.total_not_taken_pred_not_taken += 1
        else:
            self.total_not_taken_pred_taken += 1
        
        self.total_predictions += 1
