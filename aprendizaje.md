# Aprendizaje del Proyecto

En este archivo MarkDown dejare documentado, las cosas que aprendi durante el desarrollo de este proyecto, ya sea por busquedas en internet o por cosas que aparecieron en el codigo que me resultaron interesantes.

# Parámetros con llamada externa del proceso
El proceso requiere que la parametrizacion sea desde la ejecucion de Python y no modificando el código.\
Por lo que busqué y encontré lo siguiente:

`import sys`: sys guara los argumentos en una lista llamada `sys.argsv`.

** Datos Lista **
- `sys.argv[0]`: es siempre el nombre del script.
- `sys.argv[x]`: desde el 1 en adelante son los otros argumentos que se le entregan, en el caso de este proyecto el año y mes.

En caso de Error en el numero de parametros se usa:

`if len(sys.argv) != 3:
    print("Cantidad de parámetros inválidos debe ingresar año y mes.")
    sys.exit(1)`


## Descargar los origenes desde URL

`import request`: este modulo se usó en el proceso de indicadores para leer una API.

** Uso **
```respuesta = requests.get(url)
if respuesta.status_code == 200:
    with open(destino, 'wb') as f:
        f.write(respuesta.content)
else:
    print(f'Error al descargar: {respuesta.status_code}')```

## Usando duckdb
Se usa para realizar consultas SQL sobre los objetos que tenemos, por ejemplo archivos parquet, CSV, json, etc. \

Se crea una consulta SQL y luego se comecta de la siguiente forma:

'''
consulta = "SELECT campo1, campo2, campo3 FROM tabla;"

sql_base = duckdb.sql(consulta)
'''

Esto queda guardado como `DuckDBPyRelation`

Para este proyecto eso lo use para filtrar y poder realizar los select respectivos:

```sql_base = duckdb.sql(consulta)
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
 );
```


## Autor

Pedro Figueroa: desarrollador ETL con más de 20 años de experiencia en DataStage, PowerCenter, Oracle y SQL Server.
