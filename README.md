# Challenge_Solving English (in Spanish is below)
- To download the repo, click on "code" get the ssh or http, and use git clone "repo location".
- Poetry was brought to manage dependencies, therefore, creating a virtual poetry environment:
  - install poetry: pip install poetry
  - install all the dependencies of poetry, thus appearing the virtual environment: poetry install
  - Select the virtual environment to be using when running the solution.
- Docker was increased to launch a Postgres instance.
  - A docker-compose.yml will be highlighted to simplify raising the mentioned instance, run the command: docker-compose up
    - The instance will be running on port 5432 (local).
    - user:"postgres" and password:"example"
- In order to have Spark running and be able to execute that part of the solution, follow the step-by-step of the following tutorial (more or less half of it explains the step-by-step of how to do it):
  - https://sparkbyexamples.com/pyspark-tutorial/
  
## Exercise 1 - Data handling:
- a) Create the "movements" table, with the list of all Movements, with the following content: . Date . Client Description . Provider Description . Product description . Brand Description. Amount . Cost . Sale . Net income
- b) Based on the table generated in a), consult, ordering by date and description of the client: . date, customer description and profit of the first 3 operations.
- c) Given that the companies in the database belong mostly to an area with a high learning curve, it is usual that the companies do not have well calculated costs and present negative profit during their first operations.
- 1) Build a query that returns the losing marks on each of your first 3 trades.
- 2) A consultation with those who had losses in their first three operations but not in the fourth.

### Considerations Exercise 1:
  - The same thing was solved using Sql syntax. Each query inside the "Exercise 1" folder corresponds to its corresponding subparagraph.

## Exercise 2 - Python:
### Part 1:
  - For this part, pandas was used, since it is more than enough to be able to process a file of 1000 rows without too much latency (I understand this is a batch process).
  - The credentials to access the aws bucket are not found, the empty file was uploaded in case you want to replace it to test it.
  - Execution of this exercise through the command:
    - The "True" value is for whether you want to use the database or not, if "True" is not set textually, the process will be saved in s3
    - Case 1 saving in Postgres DB: "python users.py True"
    - Case 2 saving to S3: "python users.py True"
    
 ### Part 2:
  - For this part, pandas was used simply to be able to parse the file received from the API in json format (response.json()), later Spark was used for processing (both Pyspark and Spark Sql, I always find it interesting to combine both ways or keep them in mind at least given that some paths are easier one way than another, or at least for me it is).
      - Why Spark then?, because since it was requested to parameterize the request for beers to the api, 1 million could be requested, and since it can be too computational, I prefer to have distributed processing in the background so that it can handle such a volume that for example pandas could not.
  - Execution of this exercise through the command:
    - The value "80" represents the number of beers that we want to receive from the API, the value "True" that follows it, is to tell if we want to save in the DB or not (for the marketing area that is not decided)
    - Case 1 saving in Postgres DB: "python beers.py 80 True"
    - Case 2 saving in S3 and using 80 rows as parameter to request to the api: "python beers.py 80"
    - Case 3 saving in S3 and by default it will run the value it has for the number of rows: "python beers.py"
 
 ### Theoretical:
  link to Costs of S3 AWS https://aws.amazon.com/es/s3/pricing/
  - 1) First of all, if you have data that you don't use, I would start by storing it in S3 with glacier. That has very low storage costs for long times if necessary, and with rapid access recovery if desired.
       Assuming as the statement says, that you need to have access not so frequently at a reasonable price. What I would propose then is to use "S3 Intelligent - Tiering", which allows access to information that is not necessary to access frequently for a very low cost:
         - S3 Intelligent - Tiering*:
             - I quote: "S3 Intelligent-Tiering automatically stores objects in three access tiers: a hot access tier, an infrequent access tier costing 40% less than the hot access tier, and an instant access tier at files for 68% less cost than the infrequent access tier For a small monthly monitoring and automation fee per object, S3 Intelligent-Tiering monitors access patterns and moves objects that have not been accessed for 30 consecutive days at the infrequent access level and now, after 90 days without access, at the new instant file access level." (https://aws.amazon.com/es/about-aws/whats-new/2021/11/s3-intelligent-tiering-archive-instant-access-tier/)
   - 2) I would use Airflow, since I understand it is a batch process, I would use a file sensor to detect that I have a new file in a certain location, assuming it is a large file I would use spark to do the necessary processing and cleanup. I would save the file to S3 and could upload it to Hive or some other database engine that supports compute and distributed storage (as long as the database table I'm uploading it to doesn't have by location (the "location" from the table) the location where I'm leaving it in S3, otherwise it would be redundant).
   - 3) The change that I would propose is that instead of using a partition with the whole date "YYYYMMDD", I would make 3 different partitions, one that was the year - "YYYY", another the month "MM", and another the day " DD".
        In the first place, avoid the substring and cast because they are operations that can be avoided if you separate the year, month and day using them as an integer.
        Secondly, partitioning the table as mentioned, if, as in the example (the query), I consult a month, it would not be consulting the months of all the years, but could reduce the amount of metadata that is traversed behind, consulting only the months of the year that interests me, so that you want them, for example, based on the case that I say, both would remain:

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

        




# Challenge_Solving Spanish 
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
  - Para esta parte se utilizó pandas simplemente para poder parsear el archivo que se recibe de la Api en formato json (response.json()), posteriormente para el procesamiento se utilizó Spark (tanto Pyspark como Spark Sql, me parece siempre interesante combinar ambas formas o tenerlas presente almenos dado que algunos camino son más fáciles de una manera que de otra, o almenos para mí lo es).
      - ¿Por Qué Spark entonces?, por qué dado que se solicitó parametrizar la solicitud de cervezas a la api, podrían solicitarse 1 millón, y dado que puede ser demasiado cómputo, prefiero tener procesamiento distribuido de fondo para que pueda manejar semejante volumen que por ejemplo pandas no podría.
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



