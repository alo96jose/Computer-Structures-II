import math

class perceptron:
    def __init__(self, bits_to_index, global_history_size):
        self.num_perceptrons = 2 ** bits_to_index                     # Num de perceptrons: 2^n igual a al tamano de la Tabla de Percep
        self.history_size = global_history_size                       #  x_i: Bits of global branch history shift register
        self.threshold = math.floor(1.93 * global_history_size + 14)  # Calcula el umbral (threshold) con la recomendacion
        
        # Inicializandolos random disminuye el % de predicciones correctas
        # self.weights = [[random.randint(-1, 1) for _ in range(global_history_size + 1)] for _ in range(self.num_perceptrons)]
        self.weights = [[0 for _ in range(global_history_size + 1)] for _ in range(self.num_perceptrons)]
        
        # Inicializar la historia global dentro del Perceptron con ceros
        self.history = [0] * global_history_size  

        # Inicializanzo ctadores stats
        self.total_predictions = 0
        self.total_taken_pred_taken = 0
        self.total_taken_pred_not_taken = 0
        self.total_not_taken_pred_taken = 0
        self.total_not_taken_pred_not_taken = 0

    def print_info(self):
        print("Parámetros del predictor:")
        print("\tTipo de predictor:\t\t\tPerceptron")
        
        print("\tNúmero de perceptrones:\t\t\t" + str(self.num_perceptrons))
        print("\tLongitud del historial global:\t\t" + str(self.history_size))
        print("\tUmbral de decisión:\t\t\t" + str(self.threshold))

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
        index = int(PC) % self.num_perceptrons
        weights = self.weights[index]
        
        # Old version
        # y = weights[0] # Empieza con el bias weight, x_0 = 1
        # for i in range(self.history_size):
        #     # El output del Perceptron
        #     # FIXME: Este es el producto punto ver si se puede sustuir 
        #     y += weights[i + 1] * self.history[i]
        # # y: Resultado prediccion
        # if y >= 0:
        #     return "T"
        # else:
        #     return "N"
    
        # Current version: 
        # Implementando la mejora de sustituir el producto punto para calcular el output del Perceptron
        y = weights[0]  # Empieza con el bias weight, x_0 = 1
        for i in range(self.history_size):
            if self.history[i] == 1:
                y += weights[i + 1]  # Suma cuando el input_bit es 1
            else:
                y -= weights[i + 1]  # Resta cuando input_bit es -1 
        if y >= 0:
            return "T", y
        else:
            return "N", y

    def update(self, PC, result, prediction):
        index = int(PC) % self.num_perceptrons
        weights = self.weights[index]


        # Current version
        prediction, y_out = self.predict(PC)
        # t es el target de la Predicion
        # t_variable = 1 if result == "T" else -1   # Usar esta version es como 2-3 s mas lento
        if result == "T":
            t_variable = 1
        else:
            t_variable = -1

        # Training de los Pesos en el Perceptron
        # Condicional: revisa si sign (y_out) != t_variable OR si |y_out| <= threshold
        if (t_variable * y_out <= 0 or abs(y_out) <= self.threshold):
            
            weights[0] += t_variable  # Actualiza el bias weight: w_0 = t*w_o
            for i in range(1, self.history_size + 1):
                # Actualiza los pesos
                weights[i] += t_variable * self.history[i - 1] #Actualiza los pesos: w_i = w_i + t*x_i


        # Para actualizar history reg x_i equivalente a shift register
        # Apendea el valor de t_variable al final de history
        self.history.append(t_variable)
        # Condicion para botar el primer elemento para actualizar history
        if len(self.history) > self.history_size:
            self.history.pop(0)

        # Update stats
        if result == "T" and result == prediction:
            self.total_taken_pred_taken += 1
        elif result == "T" and result != prediction:
            self.total_taken_pred_not_taken += 1
        elif result == "N" and result == prediction:
            self.total_not_taken_pred_not_taken += 1
        else:
            self.total_not_taken_pred_taken += 1

        self.total_predictions += 1