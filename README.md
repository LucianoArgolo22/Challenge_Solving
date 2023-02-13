# Challenge_Solving
- Para descargar el repo, hacer click en "code" obtener el ssh o http, y usar git clone "ubicación del repo".
- Se utilizó Poetry para manejo de dependencias, por ende, crear un ambiente virtual de poetry:
  - instalar poetry: pip install poetry
  - instalar todas las dependencias de poetry generando así el ambiente virtual: poetry install
  - Seleccionar el ambiente virtual para estar usándolo a la hora de correr la solución.
- Se utilizó Docker para levantar una instancia de Postgres.
  - Se generó un docker-compose.yml para simplificar levantar la instancia mencionada, correr el comando: docker-compose up
    - La instancia va a estar corriendo en el puerto 5432 (local).
    - usuario:"postgres" y contraseña:"example"
- Para poder tener Spark corriendo y poder ejecutar esa parte de la solución, seguir el paso a paso del siguiente tutorial (masomenos por la mitad explica el paso a paso de como hacerlo):
  - https://sparkbyexamples.com/pyspark-tutorial/
        
## Ejercicio 1 - Manejo de datos:
- a) Crear la tabla “movimientos”, con el listado de todos los Movimientos, con el siguiente contenido : . Fecha . Descripción de Cliente . Descripción de Proveedor . Descripción de Producto . Descripción de Marca . Cantidad . Costo . Venta . Ganancia Neta
- b) En base a la tabla generada en a), consultar, ordenando por fecha y descripción del cliente: . fecha,  descripción de cliente y ganancia de las primeras 3 operaciones.
- c) Dado que las empresas en la base de datos pertenecen en su mayoría a un rubro con una alta curva de aprendizaje, es usual que las empresas no tengan bien calculados los costos y presenten ganancia negativa durante sus primeras operaciones.
- 1) Genere una consulta que devuelva las marcas con pérdidas en cada una de sus primeras 3 operaciones.
- 2) Una consulta con las que tuvieron pérdidas en sus primeras tres operaciones pero no en la cuarta.

### Consideraciones Ejercicio 1:
    - El mismo ser resolvió utilizando sintaxis Sql, Cada query dentro de la carpeta "Ejercicio 1" corresponde a su correspondiente inciso.

## Ejercicio 2 - Python:
### Parte 1:
    - Para esta parte se utilizó pandas, dado que es más que suficiente para poder procesar un archivo de 1000 filas sin demasiada latencia (entiendo ésto es un proceso batch).
    - Las credenciales para acceder al bucket de aws no se encuentran, se subió el archivo vacío por si quieren reemplazarse para probarlo.
    - Ejecución de éste ejercicio mediante el comando:
      -  El valor "True" es por si desea utilizarse o no la base de datos, en caso que no se ponga "True" textualmente, se guardará el proceso en s3
      -  Caso 1 guardando en Postgres DB: "python users.py True"
      -  Caso 2 guardando en S3: "python users.py True"

### Parte 2:
    - Para esta parte se utilizó pandas simplemente para poder parsear el archivo que se recibe de la Api en formato json (response.json()), posteriormente para el procesamiento se utilizó Spark (tanto Pyspark como Spark Sql, me parece siempre interesante combinar ambas formas o tenerlas presente almenos dado que algunos camino son más fáciles de una manera que de otra, o almenos para mí lo es). Al final terminé usando nuevamente Pandas, y la razón fue que no podía guardar directamente en S3 (se me complicó un poco para configurar las credenciales de aws usando spark para simplemente hacer un guardado directo desde el dataframe de spark en el bucket). 
      además almenos para éste caso fue más simple conectar con la db de presto y enviarle el dataframe de pandas para que pueda cargar la info en la tabla.
        - ¿Por Qué Spark entonces?, por qué dado que se solicitó parametrizar la solicitud de cervezas a la api, podrían solicitarse 1 millón, y dado que uso explosionado y posteriormente hago joins, prefiero tener procesamiento distribuido de fondo para que pueda manejar semejante volumen que por ejemplo pandas no podría.
    - Ejecución de éste ejercicio mediante el comando:
      - El valor "80" representa la cantidad de cervezas que queremos recibir de la Api, el valor "True" que le sigue, es para decirle si queremos guardar en la DB o no (para el área de marketing que no se decide)
      - Caso 1 guardando en Postgres DB: "python users.py 80 True"
      - Caso 2 guardando en S3 y usando como parámetro 80 rows a solicitar a la api : "python users.py 80"
      - Caso 3 guardando en S3 y por default va a correr el valor que tiene de cantidad de rows: "python users.py"

