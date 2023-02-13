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
    - Caso 1 guardando en Postgres DB: "python beers.py 80 True"
    - Caso 2 guardando en S3 y usando como parámetro 80 rows a solicitar a la api : "python beers.py 80"
    - Caso 3 guardando en S3 y por default va a correr el valor que tiene de cantidad de rows: "python beers.py"

### Teórica:
  link a Costos de S3 AWS https://aws.amazon.com/es/s3/pricing/
  - 1) En primer lugar, si se tiene data que no se usa, empezaría por almacenarla en S3 con glacier. Que tiene costos muy bajos de almacenamiento para largos tiempos si fuera necesario, y con rápida recuperación del acceso si se quisiera.
       Suponiendo como dice el enunciado, que se necesita tener acceso no tan frecuentemente a un precio razonable. Lo que propondría entonces es utilizar "S3 Intelligent - Tiering", que permite acceder a información que no es necesaria acceder de forma frecuente por muy bajo costo:
         -  S3 Intelligent - Tiering*:
             - cito: "S3 Intelligent-Tiering almacena automáticamente los objetos en tres niveles de acceso: un nivel de acceso frecuente, un nivel de acceso poco frecuente con un costo un 40 % menor que el nivel de acceso frecuente y un nivel de acceso instantáneo a los archivos con un costo un 68 % menor que el nivel de acceso poco frecuente. Por una pequeña tarifa mensual de monitoreo y automatización por objeto, S3 Intelligent-Tiering monitorea los patrones de acceso y mueve los objetos a los que no se accedió durante 30 días consecutivos al nivel de acceso poco frecuente y ahora, después 90 días sin acceso, al nuevo nivel de acceso instantáneo a los archivos." (https://aws.amazon.com/es/about-aws/whats-new/2021/11/s3-intelligent-tiering-archive-instant-access-tier/)
   - 2) Utilizaría Airflow, dado que entiendo es un proceso batch, usaría un file sensor para detectar que tengo un nuevo archivo en cierta ubicación, asumiendo que es un archivo pesado utilizaría spark para hacer el procesamiento y limpieza necesaria. Guardaría el archivo en S3 y podría cargarlo a Hive o algún otro motor de base de datos que soporte cómputo y storage distribuido (siempre y cuando la tabla de la base de datos a la que lo estoy cargando no tenga por ubicación (la "location" de la tabla) la ubicación donde lo estoy dejando en S3, sino sería redundante).
   - 3) El cambio que propondría es que en vez de usar una partición con toda la fecha entera "YYYYMMDD", haría 3 particionamientos distintos, uno que fuerea año - "YYYY", otro el mes "MM", y otro el día "DD".
        En primer lugar evitar el substring y casteo por que son operaciones que se pueden evitar si se separa en año, mes y día utilizándolos como integer. 
        En segundo lugar particionando la tabla como mencionaba, si como en el ejemplo (la query) consulto un mes, no estaría consultando los meses de todos los año, sino que podría reducir la cantidad de metadata que se recorre por detrás, consultando solo los meses del año que me interesa, por lo que las queries por ejemplo basado en el caso que digo quedarían ambas:
### DDLT:
    - CREATE EXTERNAL TABLE my_spectrum.Data_Movimientos(
      Cod_Prod integer,
      Cod_Cliente integer,
      Cantidad integer,
      Costo decimal(8,2),
      Venta decimal(8,2)
      )
      PARTITIONED BY (year int, month int, day int )  -- YYYYMMDD #YYYYMMDD #YYYYMMDD
      ROW FORMAT DELIMITED
      FIELDS TERMINATED BY '|'
      STORED AS textfile
      LOCATION 's3://bucket/spectrum/Data_Movimientos/‘
### ETL:
    - SELECT * FROM my_sepectrum.Data_Movimientos
      WHERE month >= 4 AND month <= 10

      (podría agregarse el año a menos que se quisieran saber esos intervalos de meses de todos los años)
    
    - SELECT * FROM my_sepectrum.Data_Movimientos
      WHERE year = YYYY
      and month >= 4 AND month <= 10

