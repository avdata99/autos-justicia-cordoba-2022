#Modulos importados

import json
from os import listdir
from operator import itemgetter


#Variables
archivos = listdir('data')
total = len(archivos)

#Listas
destinos = []
repeticiones = {}



#Blucle recorrido de archivos .Json Carpeta "Data"
for archivo in archivos: 
    ruta = 'data/' + archivo   

    #Apertura de archivos .Json
    with open (ruta) as contenido:
        json_data = json.load(contenido)

        #almacenas el array de vehiculos en una variable
        vehiculos = json_data['d']['ObjectData']

        #Lectura de indice 'Destino' y agregado a lista 'Destinos'
        for vehiculo in vehiculos:
            destino = (vehiculo['Destino'])
            destinos.append(destino)

        #Recorrido por lista 'destinos' y conteo de entrega a cada destino
        for cantidad in destinos:
            if cantidad in repeticiones:
                repeticiones[cantidad] +=1
            else:
                repeticiones[cantidad] = 0
                repeticiones_asc = sorted(repeticiones.items(), key=itemgetter(1))
                

        #Organiza de mayor a menor
        #repeticiones = sorted(repeticiones.items(), key=operator.itemgetter(1), reverse=True)
#print (repeticiones)
print(repeticiones_asc)
        #for name in enumerate(repeticiones):

       
        
            





#print (sorted(repeticiones.items()))
#print (repeticiones['MUNICIPALIDAD - CHILIBROSTE'])



            




        

           
        


    