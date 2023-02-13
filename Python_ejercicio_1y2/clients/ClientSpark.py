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
        df_max = self.spark.sql('''SELECT id, a.malts["name"] as principal_malt,
                        cast(substring(a.malts["amount"], 8,3) as float) as kilograms 
        from (
            select id, Explode(ingredients["malt"]) as malts from df
             ) a
        ''')
        self.log.info(f' - ClientSpark - whole_process - Grouping max values for principal_malt ')
        df2 = df_max.select('id', 'kilograms')
        df2 = df2.groupBy("id").max("kilograms").withColumnRenamed('max(kilograms)', 'kilograms')
        df2 = df_max.join(df2, ['id','kilograms'], 'inner').select('id','principal_malt').orderBy('id')
        self.log.info(f' - ClientSpark - whole_process - Joined with max values for principal_malt ')
        
        df = self.case_values(df=df, new_column_name='ph_type', column_name='ph', numeric_values=[7,7], string_values=['base', 'neutral', 'sour'])
        df = self.case_values(df=df, new_column_name='alcohol_type', column_name='abv', numeric_values=[5,7], string_values=['low', 'medium', 'strong'])
        self.log.info(f' - ClientSpark - whole_process - Performing Join ')
        df = df.join(df2, 'id', 'inner')
        return  df.select(final_columns)