
__author__ = "Georgina Salcido"
__date__ = "enero 2025"

from collections import Counter
import utileria as ut
import bosque_aleatorio as ba
import os
import random

def calcular_accuracy(validacion, prediccion):
    aciertos = sum(1 for real, pred in zip(validacion, prediccion) if real == pred)
    return aciertos / len(validacion)

url = 'https://archive.ics.uci.edu/static/public/53/iris.zip'
archivo = 'datos/iris.zip'
archivo_datos = 'datos/iris.data'
atributos = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'class']
target = 'class'

if not os.path.exists('datos'):
    os.makedirs('datos')
if not os.path.exists(archivo):
    ut.descarga_datos(url, archivo)
    ut.descomprime_zip(archivo)

datos_espacios = ut.lee_csv(archivo_datos, atributos=atributos, separador=',')
datos = [fila for fila in datos_espacios if all(fila[k] != '' for k in atributos[:-1])]

datos_transformados = [{k: float(fila[k]) for k in atributos[:-1]} | {"class": fila["class"]} for fila in datos]

# Test para ver que pasa cuando se aumenta el número de árboles, la máxima profundidad o la cantidad de variables
max_arboles = [10, 50, 200] 
max_profundidad = [None, 5, 15] 
num_variables = [1, 2, 3, 4] 

random.seed(42)
random.shuffle(datos_transformados)
N = int(0.8*len(datos))
datos_entrenamiento = datos_transformados[:N]
datos_validacion = datos_transformados[N:]

clase_default = 'Iris-versicolor'

for M in max_arboles:
    for max_prof in max_profundidad:
        for num_vars in num_variables:
            print(f"Evaluando configuración: Árboles={M}, Profundidad={max_prof}, Variables por nodo={num_vars}")
            
            bosque = ba.entrena_bosque(
                datos = datos_entrenamiento,  
                target = target,
                clase_default = clase_default,
                M=M,
                max_profundidad=max_prof,
                variables_seleccionadas=num_vars
            )

            predicciones = [ba.predice_bosque(bosque, instancia) for instancia in datos_validacion]
            
            # Evalía precisión
            valida_real = [fila[target] for fila in datos_validacion]
            precision = calcular_accuracy(valida_real, predicciones)

            print(f"Precisión: {precision:.4f}")