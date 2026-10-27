import requests
import time

import pandas as pd

from pathlib import Path

url = "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"

raiz = Path(__file__).resolve().parent.parent

f_bronze = raiz / "data" / "bronze" / "lookup" / "taxi_zone_lookup.csv"


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
            print(f"Intento {intento} de {intentos} falló: {error}.")
            if intento < intentos:
                time.sleep(espera*intento)
    raise RuntimeError(
        f"No se pudo extraer {url} después de {intentos} intentos.")


def contar_lineas(archivo):
    df = pd.read_csv(archivo)
    cant_lineas = len(df)
    print(
        f"el archivo lookup de Taxi_Zone tiene {cant_lineas} líneas.")
    return cant_lineas


if __name__ == "__main__":
    descarga_archivo(url, f_bronze)
    contar_lineas(f_bronze)
