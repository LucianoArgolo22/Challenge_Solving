from pyspark.sql import SparkSession
from pyspark.sql.functions import when
import pandas as pd

class ClientSpark:
    def __init__(self, log:object):
        self.log = log
        self.spark = self.initializing_session()
        
    def initializing_session(self) -> object:
        self.log.info(f' - ClientSpark - initializing session - creating spark session')
        return SparkSession.builder \
            .master("local[1]") \
            .appName("SparkByExamples.com") \
            .getOrCreate() 

    def case_values(self, df:object, new_column_name:str, column_name:str, numeric_values:list=[0,2], string_values:list=['lower','medium','higher'] ) -> object:
        self.log.info(f' - ClientSpark - case_values - generating new column {new_column_name} with cases from column {column_name}')
        return df.withColumn(new_column_name,    when(df[column_name] < numeric_values[0], string_values[0])
                                 .when( (df[column_name] >= numeric_values[0]) & (df[column_name] <= numeric_values[1]), string_values[1])
                                 .when(df[column_name] == 'NaN'  ,"not found")
                                 .when(df[column_name].isNull()  ,"not found")
                                 .when(df[column_name] > numeric_values[1], string_values[2]) )
    
    def whole_process(self, df:pd.DataFrame, initial_columns:list, final_columns:list) -> object:
        self.log.info(f' - ClientSpark - whole_process - Running whole processing ')
        df = self.spark.createDataFrame(df)
        df = df.select(initial_columns)
        df.createOrReplaceTempView('df')
        df = self.spark.sql('''SELECT *, a.malts["name"] as principal_malt,
                                    cast(substring(a.malts["amount"], 8,3) as float) as kilograms 
                        from (
                                select *, Explode(ingredients["malt"]) as malts from df
                             ) a
        ''')
        self.log.info(f' - ClientSpark - whole_process - obtaining max values for principal_malt ')
        df = df.select(['id', 'name', 'first_brewed', 'abv', 'ibu', 'ph','principal_malt', 'kilograms'])
        df.createOrReplaceTempView('df2')
        df = self.spark.sql('''select * 
            from (
                    select 
                    *,
                    row_number() over (partition by id order by id, kilograms desc) as max_malt
                    from df2 
                ) a
            where max_malt = 1
            ''')
        df = self.case_values(df=df, new_column_name='ph_type', column_name='ph', numeric_values=[7,7], string_values=['base', 'neutral', 'sour'])
        df = self.case_values(df=df, new_column_name='alcohol_type', column_name='abv', numeric_values=[5,7], string_values=['low', 'medium', 'strong'])
        self.log.info(f' - ClientSpark - whole_process - Returning df ')
        return  df.select(final_columns)
