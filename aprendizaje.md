# Aprendizaje del Proyecto

En este archivo MarkDown dejare documentado, las cosas que aprendi durante el desarrollo de este proyecto, ya sea por busquedas en internet o por cosas que aparecieron en el codigo que me resultaron interesantes.

# Parámetros con llamada externa del proceso
El proceso requiere que la parametrizacion sea desde la ejecucion de Python y no modificando el código.\
Por lo que busqué y encontré lo siguiente:

`import sys`: sys guara los argumentos en una lista llamada `sys.argsv`.

** Datos Lista **
- `sys.argv[0]`: es siempre el nombre del script.
- `sys.argv[x]`: desde el 1 en adelante son los otros argumentos que se le entregan, en el caso de este proyecto el año y mes.

## Descargar los origenes desde URL

`import request`: este modulo se usó en el proceso de indicadores para leer una API.

** Uso **
```respuesta = requests.get(url)
if respuesta.status_code == 200:
    with open(destino, 'wb') as f:
        f.write(respuesta.content)
else:
    print(f'Error al descargar: {respuesta.status_code}')```


## Autor

Pedro Figueroa: desarrollador ETL con más de 20 años de experiencia en DataStage, PowerCenter, Oracle y SQL Server.
