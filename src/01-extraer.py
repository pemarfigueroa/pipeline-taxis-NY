import requests  # Para buscar los origenes en URL.
import pandas as pd  # Se usa Pandas para leer parquet y poder contar lineas.
import sys       # Para leer los parametros de ejecucion.
# para determinar el tiempo de espera entre reintentos de descarga.
import time

from pathlib import Path

# Declaracion de parametros de entrada
p_year = sys.argv[1]
p_month = sys.argv[2]

# Declaracion de parametros del proceso
url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{p_year}-{p_month.zfill(2)}.parquet"

raiz = Path(__file__).resolve().parent.parent

f_bronze = raiz / "data" / "bronze" / \
    f"year={p_year}" / f"month={p_month}" / \
    f"yellow_tripdata_{p_year}-{p_month.zfill(2)}.parquet"


def valida_param(v_year, v_month):
    v_valido = False
    if int(v_year) in range(2009, 2027):
        if int(v_year) == 2026 and int(v_month) in range(1, 9):
            v_valido == True
        elif int(v_month) in range(1, 13):
            v_valido = True
    if not (v_valido):
        print(
            f"Parámetros Año: {v_year} y/o Mes: {v_month} ingresados no válidos.")
    return v_valido


def descarga_archivo(url, destino, intentos=3, espera=5):
    # Permite crear las carpetas HIVE, si es que no existen
    destino.parent.mkdir(parents=True, exist_ok=True)
    # Proceso de descarga del archivo
    for intento in range(1, intentos):
        try:
            respuesta = requests.get(url, timeout=10)
            respuesta.raise_for_status()
            with open(destino, 'wb') as f:
                f.write(respuesta.content)
            return respuesta.content
        except requests.exceptions.RequestException as error:
            print(f"Intento {intento} de {intentos} falló: {error}")
            if intento < intentos:
                time.sleep(espera*intento)
    raise RuntimeError(
        f"No se pudo extraer {url} después de {intentos} intentos")


def contar_lineas(archivo, v_year, v_month):
    df = pd.read_parquet(archivo)
    cant_lineas = len(df)
    print(
        f"el archivo del periodo {str(v_year) + v_month.zfill(2)} tiene {cant_lineas} lineas")
    return cant_lineas


if valida_param(p_year, p_month):
    descarga_archivo(url, f_bronze)
    contar_lineas(f_bronze, p_year, p_month)


# Falta agregar el conteo de registros que hay en el parquet.
