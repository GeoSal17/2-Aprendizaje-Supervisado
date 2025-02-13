
__author__ = "Georgina Salcido"
__date__ = "enero 2025"

from collections import Counter
import utileria as ut
import bosque_aleatorio as ba
import os
import random

# Función para calcular la exactitud del árbol según las configuraciones dadas.
def calcular_accuracy(validacion, prediccion):
    aciertos = sum(1 for real, pred in zip(validacion, prediccion) if real == pred)
    return aciertos / len(validacion)

# Manejo de las datasets (yo puse 2 ejemplos, solo es necesario cambiar los comentarios de prueba_BA.py)
url = 'https://archive.ics.uci.edu/static/public/53/iris.zip'
archivo = 'datos/iris.zip'
archivo_datos = 'datos/iris.data'
atributos = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'class']
target = 'class'
"""
url = 'https://archive.ics.uci.edu/static/public/176/blood+transfusion+service+center.zip'
archivo = 'datos/transfusion.zip'
archivo_datos = 'datos/transfusion.data'
atributos = ['Recency', 'Frequency', 'Monetary', 'Time', 'Donated_Blood']
target = 'Donated_Blood'
"""

if not os.path.exists('datos'):
    os.makedirs('datos')
if not os.path.exists(archivo):
    ut.descarga_datos(url, archivo)
    ut.descomprime_zip(archivo)

datos_espacios = ut.lee_csv(archivo_datos, atributos=atributos, separador=',')
datos = [fila for fila in datos_espacios if all(fila[k] != '' for k in atributos[:-1])]

datos_transformados = [{k: float(fila[k]) for k in atributos[:-1]} | {"class": fila["class"]} for fila in datos]
#datos_transformados = [{k: float(fila[k]) for k in atributos[:-1]} | {"Donated_Blood": fila["Donated_Blood"]} for fila in datos]

# Test para ver que pasa cuando se aumenta el número de árboles, la máxima profundidad o la cantidad de variables
max_arboles = [10, 50, 100] 
max_profundidad = [None, 10, 20] 
num_variables = [1, 2, 3, 4] 

random.seed(42)
random.shuffle(datos_transformados)
N = int(0.8*len(datos))
datos_entrenamiento = datos_transformados[:N]
datos_validacion = datos_transformados[N:]

clase_default = 'Iris-versicolor'
#clase_default = '1'

resultados = []
print('Árboles'.center(10) + 'Profundidad'.center(15) + 'Variables'.center(15) + 'Accuracy'.center(15))
print('-' * 55)

for M in max_arboles:
    for max_prof in max_profundidad:
        for num_vars in num_variables:
            #print(f"Evaluando configuración: Árboles={M}, Profundidad={max_prof}, Variables por nodo={num_vars}")
            
            bosque = ba.entrena_bosque(
                datos = datos_entrenamiento,  
                target = target,
                clase_default = clase_default,
                M=M,
                max_profundidad=max_prof,
                variables_seleccionadas=num_vars
            )

            predicciones = [ba.predice_bosque(bosque, instancia) for instancia in datos_validacion]
            
            valida_real = [fila[target] for fila in datos_validacion]
            precision = calcular_accuracy(valida_real, predicciones)
            resultados.append((M, max_prof, num_vars, precision))

            #print(f"Precisión: {precision:.4f}")
            print(
                f'{M}'.center(10) 
                + f'{str(max_prof) if max_prof is not None else "None"}'.center(15) 
                + f'{num_vars}'.center(15) 
                + f'{precision:.4f}'.center(15)
            )

print('-' * 55 + '\n')
mejor_config = max(resultados, key=lambda x: x[3])
print(f"La configuración con mayor precisión es:")
print(f"Árboles: {mejor_config[0]}, Profundidad: {mejor_config[1]}, Variables: {mejor_config[2]}, Precisión: {mejor_config[3]:.4f}" + '\n')
print('-' * 55 + '\n')