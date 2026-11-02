# pipeline-taxis-NY
Proyecto personal de estudio, usando datos de Taxis amarillos de New York.

## .gitignore
Se define que ni datos ni archivos duckdb se versionan.

## Proceso de extraccion Data Taxi Amarillo a Bronze
En este proceso se extrae la data desde el origen, y se almacena en sus respectivas capetas usando Particionamiento HIVE.

** Ejecución **
- `python src/01-extraer.py 2025 1` \
   Resutado: el archivo del periodo 202501 tiene 3475226 lineas.
- `python src/01-extraer.py 2025 2` \
   Resultado: el archivo del periodo 202502 tiene 3577543 lineas.
- `python src/01-extraer.py 2025 3` \
   Resultado: el archivo del periodo 202503 tiene 4145257 lineas.

## Proceso de extraccion de Datos de Taxi_Zone.
Se extraen los datos de la tabla lookup de Taxi_zone que viene en csv, y se almacena en la carpeta lookup dentro de Data.

** Ejecución **
- `python src/01b-extraer_taxi_zone.py` \
   Respuesta: el archivo lookup de Taxi_Zone tiene 265 lineas

### Imagenes Datos en Bronze

![Datos en Bronze](img/Paso_01_extraccion_bronze.png)

## Proceso de Validación de los datos en archivos Bronze
Proceso que realiza la validacion y limpieza de los datos del archivo en bronze.

Solicitud recibida de validacion de registros:

| Código | Regla de rechazo                          |
|:------:|:------------------------------------------|
| V01    | La fecha de inicio no corresponde al mes del archivo |
| V02    | La fecha de fin es anterior o igual a la de inicio |
| V03    | El viaje dura más de 24 horas |
| V04    | Distancia menor o igual a cero |
| V05    | Tarifa (fare_amount) o total (total_amount)negativos |
| V06    | Zona de origen o destino que no existe en la tablade zonas |
| V07    | Forma de pago fuera de los códigos del diccionario |
| V08    | Pasajeros igual a cero |
| V09    | Registro duplicado exacto: se acepta uno, el resto se rechaza |

** Ejecución del proceso **
- `python src/02-validar-origen.py 2025 1` \
   Resultado: 
   - El archivo cuarentena tiene 246088 líneas.
   - El archivo limpio tiene 3229138 líneas.

   Detalle cod_rechazo:
┌─────────────┬──────────────────┐
│ cod_rechazo │ AScant_registros │
│   varchar   │      int64       │
├─────────────┼──────────────────┤
│ V01         │               22 │
│ V02         │             1797 │
│ V03         │               18 │
│ V04         │            90880 │
│ V05         │           129723 │
│ V08         │            23648 │
└─────────────┴──────────────────┘
- `python src/02-validar-origen.py 2025 2`
   Resultado:
   - El archivo cuarentena tiene 246088 líneas.
   - El archivo limpio tiene 3229138 líneas.

   Detalle por cod_rechazo:
┌─────────────┬──────────────────┐
│ cod_rechazo │ AScant_registros │
│   varchar   │      int64       │
│ V01         │               22 │
│ V02         │             1797 │
│ V03         │               18 │
│ V04         │            90880 │
│ V05         │           129723 │
│ V08         │            23648 │
└─────────────┴──────────────────┘

- `python src/02-validar-origen.py 2025 3`
   Resultado:
   - El archivo cuarentena tiene 318260 líneas.
   - El archivo limpio tiene 3826997 líneas.

   Detalle por cod_rechazo:
┌─────────────┬──────────────────┐
│ cod_rechazo │ AScant_registros │
│   varchar   │      int64       │
├─────────────┼──────────────────┤
│ V01         │               33 │
│ V02         │              975 │
│ V03         │                9 │
│ V04         │           103719 │
│ V05         │           192131 │
│ V08         │            21393 │
└─────────────┴──────────────────┘

## Imagenes de Validación a Silver

![Datos en Silver](img/Paso_02_Validacion_y_Silver.png)

#### Por el momento estos son los modulos que se requieren instalar
#### Claude esto no considerarlo por ahora
- `pip install requests`
- `pip install pandas pyarow`
- `pip install duckdb`