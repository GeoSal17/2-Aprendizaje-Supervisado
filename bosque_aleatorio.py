
__author__ = "Georgina Salcido"
__date__ = "enero 2025"


import random
from arboles_numericos import entrena_arbol

def entrena_bosque(datos, target, clase_default, M,
                            max_profundidad=None, acc_nodo=1.0, min_ejemplos=0,
                            variables_seleccionadas=None):
    subconjuntos = [random.sample(datos, k=len(datos)) for _ in range(M)]
    #subconjuntos = [random.choices(datos, k=len(datos)) for _ in range(M)]

    for i, subset in enumerate(subconjuntos):
        #print(f"🌲 Árbol {i+1} - Tamaño del subconjunto: {len(subset)}")
        if len(subset) == 0:
            print(f"⚠️ Error: El subconjunto {i+1} está vacío")

    bosque = [
        entrena_arbol(subset, target, clase_default,
                      max_profundidad, acc_nodo, min_ejemplos, variables_seleccionadas)              
        #for subset in subconjuntos
    ]
    return bosque

def predice_arbol(nodo, instancia):
    if (nodo.terminal): 
        return nodo.clase_default
    if instancia[nodo.atributo] < nodo.valor:
        return predice_arbol(nodo.hijo_menor, instancia)
    else:
        return predice_arbol(nodo.hijo_mayor, instancia)
    
def predice_bosque(bosque, instancia):
    predicciones = [predice_arbol(arbol, instancia) for arbol in bosque]
    return find_most_common(predicciones)

#Sacado de reddit jejejejej @kuzmovych_y
def find_most_common(num_list: list):
    counts = {}
    for n in num_list:
        counts[n] = counts.get(n, 0) + 1
    return max(counts, key=counts.get)
