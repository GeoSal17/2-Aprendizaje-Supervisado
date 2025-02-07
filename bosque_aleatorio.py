import random
from arboles_numericos import entrena_arbol

def entrena_BosqueA(datos, M, target, clase_default,
                            max_profundidad=None, acc_nodo=1.0, min_ejemplos=0,
                            variables_seleccionadas=None):
    
    subconjuntos = [random.choices(datos, k=len(datos)) for _ in range(M)]
    bosque = [
        entrena_arbol(datos, target, clase_default,
                      max_profundidad, acc_nodo, min_ejemplos, variables_seleccionadas)
        for subset in subconjuntos
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
