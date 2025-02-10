"""
Este archivo contiene funciones que se utilizan en el miniproyecto.

Como leer archivos de datos y formatearlos para que sean utilizados en los algoritmos.
"""

from urllib3 import request
import urllib.request
import zipfile

def descarga_datos(url, archivo):
    """
    Descarga un archivo de datos de una URL.
    
    Parámetros
    ----------
    url : str
        URL de donde se descargará el archivo.
    archivo : str
        Nombre del archivo donde se guardará la descarga.
    """
    urllib.request.urlretrieve(url, archivo)
    return None

def descomprime_zip(archivo, directorio='datos'):
    """
    Descomprime un archivo zip.
    
    Parámetros
    ----------
    archivo : str
        Nombre del archivo zip.
    directorio : str
        Directorio donde se descomprimirá el archivo.
    """
    with zipfile.ZipFile(archivo, 'r') as zip_ref:
        zip_ref.extractall(directorio)
    return None

def lee_csv(archivo, atributos=None, separador=','):
    """
    Lee un archivo CSV y regresa una lista de diccionarios.
    Detecta si la primera línea contiene cabecera y la omite si es necesario.

    Parámetros
    ----------
    archivo : str
        Nombre del archivo CSV.
    atributos : list(str) o None
        Lista de atributos a considerar. Si es None, intenta detectar si el archivo tiene cabecera.
    separador : str
        Separador de columnas.

    Retorna
    -------
    list[dict]
        Lista de diccionarios con los datos del CSV.
    """
    with open(archivo, 'r', encoding='utf-8') as f:
        lineas = [l.strip() for l in f.readlines() if l.strip()]

    primera_fila = [valor.strip().replace('"', '') for valor in lineas[0].split(separador)]

    if atributos is None:
        if all(any(c.isalpha() for c in valor) for valor in primera_fila):
            columnas = primera_fila
            lineas = lineas[1:]
        else:
            columnas = [f"col_{i}" for i in range(len(primera_fila))]
    else:
        if all(any(c.isalpha() for c in valor) for valor in primera_fila):
            columnas = primera_fila
            lineas = lineas[1:]
        if primera_fila == atributos:
            lineas = lineas[1:] 
        columnas = atributos

    datos = []
    for l in lineas:
        valores = [v.strip().replace('"', '') for v in l.split(separador)]
        if len(valores) == len(columnas): 
            datos.append({c: v for c, v in zip(columnas, valores)})
    
    return datos
