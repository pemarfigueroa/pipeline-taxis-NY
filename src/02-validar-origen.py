import sys

import pandas as pd

from pathlib import Path


p_year = sys.argv[1]
p_month = sys.argv[2]


raiz = Path(__file__).resolve().parent.parent

f_bronze = raiz / "data" / "bronze" / \
    f"year={p_year}" / f"month={p_month}" / \
    f"yellow_tripdata_{p_year}-{p_month.zfill(2)}.parquet"

f_silver = raiz / "data" / "silver" / \
    f"year={p_year}" / f"month={p_month.zfill(2)}" / \
    f"viajes_taxi_{p_year}-{p_month.zfill(2)}.parquet"

f_cuarentena = raiz / "data" / "silver" / \
    f"year={p_year}estandar_parquet" / f"month={p_month.zfill(2)}" / \
    f"cuarentena_{p_year}-{p_month.zfill(2)}."


def estandar_parquet(archivo):
    df = pd.read_parquet(archivo)
    df.columns = ["id_proveedor", "fecha_inicio_taximetro", "fecha_fin_taximetro", "cant_pasajeros", "distancia_viaje", "id_final_tarifa", "flag_almac_memoria", "id_zona_origen", "id_zona_destino",
                  "tipo_pago", "tarifa_taximeto", "recargos_extra", "impto_tarifa", "monto_propina", "monto_total_peajes", "recargo_mejoras", "monto_total", "recargo_congestion", "tarifa_aeropuerto", "tarifa_congest_cbd"]

    return df


if __name__ == "__main__":

    df = estandar_parquet(f_bronze)
    print(df.dtypes)
