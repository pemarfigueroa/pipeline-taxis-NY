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
    f"year={p_year}" / f"month={p_month.zfill(2)}" / \
    f"cuarentena_{p_year}-{p_month.zfill(2)}."


# def cambia_nombres(df):
#     # para modificar los nombres de las columnas aun estandar.

#     return df_aux


# def valida_lineas(df):

#     return df_quar


if __name__ == "__main__":

    df = pd.read_parquet(f_bronze)
    print(df.dtypes)
