class pshared:
    def __init__(self, bits_to_index, local_history_size):
        # Escriba aquí el init de la clase
        self.bits_to_index = bits_to_index # The PC
        self.local_history_size = local_history_size
        self.size_of_pattern_table = 2**local_history_size
        self.size_of_history_table = 2**bits_to_index

        # Se inicializa pattern_table con predictores 2 bits en 00
        self.pattern_table = [0 for i in range(self.size_of_pattern_table)]

        # Se inicializa history_table con local history registers
        #self.history_table = [0 for j in range(self.size_of_history_table)]

        # Habrá problema si Branch PC > Local History Size?
        #if self.local_history_size > self.bits_to_index:
         #   print("El tamaño del registro de historia es mayor que los bits para indexar la tabla, se limitará el registro a "+str(self.bits_to_index)+ "bits")
          #  self.local_history_size = self.bits_to_index

        self.local_history_reg = ""
        for x in range(local_history_size):
            self.local_history_reg += "0"

        # Se inicializa history_table con local history registers
        self.history_table = [self.local_history_reg for j in range(self.size_of_history_table)]


        self.total_predictions = 0
        self.total_taken_pred_taken = 0
        self.total_taken_pred_not_taken = 0
        self.total_not_taken_pred_taken = 0
        self.total_not_taken_pred_not_taken = 0

    def print_info(self):
        print("Parámetros del predictor:")
        print("\tTipo de predictor:\t\t p-shared")

    def print_stats(self):
        print("Resultados de la simulación")
        print("\t# branches:\t\t\t\t\t\t"+str(self.total_predictions))
        print("\t# branches tomados predichos correctamente:\t\t"+str(self.total_taken_pred_taken))
        print("\t# branches tomados predichos incorrectamente:\t\t"+str(self.total_taken_pred_not_taken))
        print("\t# branches no tomados predichos correctamente:\t\t"+str(self.total_not_taken_pred_not_taken))
        print("\t# branches no tomados predichos incorrectamente:\t"+str(self.total_not_taken_pred_taken))
        perc_correct = 100*(self.total_taken_pred_taken+self.total_not_taken_pred_not_taken)/self.total_predictions
        formatted_perc = "{:.3f}".format(perc_correct)
        print("\t% predicciones correctas:\t\t\t\t"+str(formatted_perc)+"%")

    def predict(self, PC):
        PC_index = int(PC) % self.size_of_history_table
        # Será la siguiente línea necesaria en predict?
        #LHR_index = int(self.local_history_reg,2)

        #print("Predict")
        #print(PC_index,LHR_index)
        #print(PC_index)
        #print(bin(PC_index),bin(LHR_index))
        #print(bin(PC_index))

        # Primero se busca en history_table indexando con PC_index: 
        history_table_entry = self.history_table[PC_index]

        # 
        LHR_index = int(history_table_entry,2)

        # Segundo se busca en pattern_table indexando con la entrada 
        # history_table_entry 
        pattern_table_entry = self.pattern_table[LHR_index]
        #print("Pattern table entry: ")
        #print(pattern_table_entry)
        #print("History table entry: ")
        #print(history_table_entry)

        if pattern_table_entry in [0,1]:
            return "N"
        else:
            return "T"


    def update(self, PC, result, prediction):
        PC_index = int(PC) % self.size_of_history_table
        #LHR_index = int(self.local_history_reg,2)

        #print("Update")
        #print(PC_index,LHR_index)
        #print(bin(PC_index),bin(LHR_index))
        #print("PC_index: ", PC_index)
        #print("PC_index_binario: ",bin(PC_index))

        # Se agrega local_history_reg a history_table
        # self.history_table[PC_index] = LHR_index

        history_table_entry = self.history_table[PC_index]
        LHR_index = int(history_table_entry,2)
        pattern_table_entry = self.pattern_table[LHR_index]

        #print("Pattern table entry: ")
        #print(pattern_table_entry)
        #print("History table entry: ")
        #print(history_table_entry)

        # Update entry accordingly in Patter Table
        if pattern_table_entry == 0 and result == "N":
            updated_pattern_table_entry = pattern_table_entry
            #print(PC,LHR_index,pattern_table_entry,updated_pattern_table_entry,result,prediction)
        elif pattern_table_entry != 0 and result == "N":
            updated_pattern_table_entry = pattern_table_entry - 1
            #print(PC,LHR_index,pattern_table_entry,updated_pattern_table_entry,result,prediction)
        elif pattern_table_entry == 3 and result == "T":
            updated_pattern_table_entry = pattern_table_entry
            #print(PC,LHR_index,pattern_table_entry,updated_pattern_table_entry,result,prediction)
        else:
            updated_pattern_table_entry = pattern_table_entry + 1
            #print(PC,LHR_index,pattern_table_entry,updated_pattern_table_entry,result,prediction)

        #self.pattern_table[LHR_index] = updated_pattern_table_entry
        #self.pattern_table[history_table_entry] = updated_pattern_table_entry
        self.pattern_table[LHR_index] = updated_pattern_table_entry

        #print("pattern_table_entry :")
        #print(pattern_table_entry)

        # Update LHR
        if result == "T":

            #self.local_history_reg = self.local_history_reg[-self.local_history_size+1:] + "1"
            history_table_entry = history_table_entry[-self.local_history_size+1:] + "1"
        else:
            #self.local_history_reg = self.local_history_reg[-self.local_history_size+1:] + "0"
            history_table_entry= history_table_entry[-self.local_history_size+1:] + "0"

        # Se actualiza la history_table  
        #history_table_entry = int(self.local_history_reg,2) #?????
        #LHR_index = int(self.local_history_reg,2)
        self.history_table[PC_index] = history_table_entry

        #print("LHR = "+self.local_history_reg)
        #print("LHR = "+history_table_entry)

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
