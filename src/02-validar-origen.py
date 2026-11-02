import duckdb
import sys
import calendar
import pandas as pd

from datetime import datetime, date
from pathlib import Path

if len(sys.argv) != 3:
    print("Cantidad de parámetros inválidos debe ingresar año y mes.")
    sys.exit(1)

p_year = sys.argv[1]
p_month = sys.argv[2]

v_fecha_ejec = date.today()
raiz = Path(__file__).resolve().parent.parent

f_bronze = raiz / "data" / "bronze" / \
    f"year={p_year}" / f"month={p_month}" / \
    f"yellow_tripdata_{p_year}-{p_month.zfill(2)}.parquet"

f_lookup = raiz / "data" / "bronze" / \
    "lookup" / \
    "taxi_zone_lookup.csv"

f_silver = raiz / "data" / "silver" / \
    f"year={p_year}" / f"month={p_month}" / \
    f"viajes_taxi_{p_year}-{p_month.zfill(2)}.parquet"

f_cuarentena = raiz / "data" / "silver" / \
    f"year={p_year}" / f"month={p_month}" / \
    f"cuarentena_{p_year}-{p_month.zfill(2)}.csv"

sql_bronze = f"""WITH 
    cte_bronze AS (SELECT VendorID AS id_proveedor,
                          tpep_pickup_datetime AS fecha_inicio_taximetro,
                          tpep_dropoff_datetime AS fecha_fin_taximetro,
                          passenger_count AS cant_pasajeros,
                          trip_distance AS distancia_viaje,
                          RatecodeID AS id_final_tarifa,
                          store_and_fwd_flag AS flag_almac_memoria,
                          PULocationID AS id_zona_origen,
                          DOLocationID AS id_zona_destino,
                          payment_type AS tipo_pago,
                          fare_amount AS tarifa_taximeto,
                          extra AS recargos_extra,
                          mta_tax AS impto_tarifa,
                          tip_amount AS monto_propina,
                          tolls_amount AS monto_total_peajes,
                          improvement_surcharge AS recargo_mejoras,
                          total_amount AS monto_total,
                          congestion_surcharge AS recargo_congestion,
                          airport_fee AS tarifa_aeropuerto,
                          cbd_congestion_fee AS tarifa_congest_cbd,
                          ROW_NUMBER() OVER(PARTITION BY VendorID, tpep_pickup_datetime, tpep_dropoff_datetime,passenger_count, trip_distance, RatecodeID, store_and_fwd_flag, PULocationID, DOLocationID, payment_type, fare_amount, extra, mta_tax, tip_amount, tolls_amount, improvement_surcharge, total_amount, congestion_surcharge, airport_fee, cbd_congestion_fee) AS cont_duplicado
                     FROM read_parquet('{f_bronze}', hive_partitioning=True) B
                  ),
    lkp_origen AS (SELECT LocationID AS id_origen
                     FROM read_csv('{f_lookup}', hive_partitioning=True)),
    lkp_destino AS (SELECT LocationID AS id_destino
                     FROM read_csv('{f_lookup}', hive_partitioning=True))

SELECT id_proveedor,
       fecha_inicio_taximetro,
       fecha_fin_taximetro,
       cant_pasajeros,
       distancia_viaje,
       id_final_tarifa,
       flag_almac_memoria,
       id_zona_origen,
       id_zona_destino,
       tipo_pago,
       tarifa_taximeto,
       recargos_extra,
       impto_tarifa,
       monto_propina,
       monto_total_peajes,
       recargo_mejoras,
       monto_total,
       recargo_congestion,
       tarifa_aeropuerto,
       tarifa_congest_cbd,
       CASE 
          WHEN strftime(fecha_inicio_taximetro, '%Y%m') <> {p_year}{p_month.zfill(2)} THEN 'V01'
          WHEN strftime(fecha_fin_taximetro, '%Y%m') <> {p_year}{p_month.zfill(2)} THEN 'V02'
          WHEN datediff('hour', fecha_inicio_taximetro, fecha_fin_taximetro) > 24 THEN 'V03'
          WHEN distancia_viaje <= 0 THEN 'V04'
          WHEN (tarifa_taximeto < 0) OR (monto_total < 0) THEN 'V05'
          WHEN O.id_origen IS NULL OR D.id_destino IS NULL THEN 'V06'
          WHEN tipo_pago NOT IN RANGE(0,7) THEN 'V07'
          WHEN cant_pasajeros <= 0 THEN 'V08'
          WHEN cont_duplicado > 1 THEN 'V09' 
          ELSE 'V00'
       END AS cod_rechazo,
       '{v_fecha_ejec}' as fecha_ejecucion
  FROM cte_bronze B
    LEFT JOIN lkp_origen AS O
          ON  B.id_zona_origen = O.id_origen
    LEFT JOIN lkp_destino AS D
          ON  B.id_zona_destino = D.id_destino;"""


def guardar_cuarentena(consulta, arch_cuaretn):
    # Para guardar los datos de cuarentena
    sql_base = duckdb.sql(consulta)
    rel_rech = (
        sql_base
        .select("""id_proveedor, fecha_inicio_taximetro,
                fecha_fin_taximetro, cant_pasajeros,
                distancia_viaje, id_final_tarifa,
                flag_almac_memoria, id_zona_origen,
                id_zona_destino, tipo_pago, 
                tarifa_taximeto, recargos_extra,
                impto_tarifa, monto_propina,
                monto_total_peajes, recargo_mejoras,
                monto_total, recargo_congestion,
                tarifa_aeropuerto, tarifa_congest_cbd,
                cod_rechazo, fecha_ejecucion""")
        .filter("cod_rechazo <> 'V00'")
     ) 
    arch_cuaretn.parent.mkdir(parents=True, exist_ok=True)
    rel_rech.write_csv(arch_cuaretn)

def guardar_datos_silver(consulta, archivo):
    # Para guardar los datos de cuarentena
    sql_base = duckdb.sql(consulta)
    rel_rech = (
        sql_base
        .filter("cod_rechazo == 'V00'")
        .select("""id_proveedor, fecha_inicio_taximetro,
                fecha_fin_taximetro, cant_pasajeros,
                distancia_viaje, id_final_tarifa,
                flag_almac_memoria, id_zona_origen,
                id_zona_destino, tipo_pago, 
                tarifa_taximeto, recargos_extra,
                impto_tarifa, monto_propina,
                monto_total_peajes, recargo_mejoras,
                monto_total, recargo_congestion,
                tarifa_aeropuerto, tarifa_congest_cbd""")
     ) 
    archivo.parent.mkdir(parents=True, exist_ok=True)
    rel_rech.write_parquet(archivo)

def validar_archivos(arch_final, arch_rech):
    df_rech = pd.read_csv(arch_rech)
    lineas_rech = len(df_rech)
    print(f"El archivo cuarentena tiene {lineas_rech} líneas.")
    df_base = pd.read_parquet(arch_final)
    lineas_base = len(df_base)
    print(f"El archivo limpio tiene {lineas_base} líneas.")

def detalle_cuarentena(archivo):
    consulta = f"""SELECT cod_rechazo, COUNT(1) AScant_registros
                    FROM read_csv('{archivo}')
                   GROUP BY cod_rechazo
                   ORDER BY cod_rechazo;"""
    duckdb.sql(consulta).show()

if __name__ == "__main__":
    # creo variables para el proceso
    guardar_cuarentena(sql_bronze, f_cuarentena)
    guardar_datos_silver(sql_bronze, f_silver)
    validar_archivos(f_silver, f_cuarentena)
    detalle_cuarentena(f_cuarentena)
