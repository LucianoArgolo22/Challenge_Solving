#%%
from clients.ClientLogger import ClientLogger
from clients.ClientSesPSQL import ClientPSQL
from clients.ClientS3 import ClientS3
from clients.ClientProcessing import ClientProcessing
import pandas as pd


#%%
logger = ClientLogger(filename='spark_s3.log', app_name='spark_s3')
log = logger.get_log()
df = pd.read_json('parsed.json')
psql = ClientPSQL(log=log, table='beers', df=df )
psql.inserting_rows()
#%%

logger = ClientLogger(filename='parser_s3.log', app_name='parser_s3')
log = logger.get_log()
clients3 = ClientS3(log=log, python='python1')
file = clients3.get_file()
process = ClientProcessing(log=log)
df = process.whole_processing(file=file, dataframe=True)
#%%
