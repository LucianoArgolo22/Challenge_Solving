from clients.ClientSpark import ClientSpark
from clients.ClientLogger import ClientLogger
from clients.ClientSesPSQL import ClientPSQL
from clients.ClientS3 import ClientS3
import pandas as pd
import requests
import sys


if __name__=='__main__':
    logger = ClientLogger(filename='spark_s3.log', app_name='spark_s3')
    log = logger.get_log()

    log.info(f' arguments inserted: {sys.argv}')

    total_beers = sys.argv[1] if len(sys.argv) == 2 else 80
    database = True if len(sys.argv) == 2 and sys.argv[1] == 'True'  else False
    response = requests.get(f'https://api.punkapi.com/v2/beers?per_page={total_beers}')
    
    initial_columns = ['id', 'name', 'first_brewed', 'abv', 'ibu', 'ph', 'ingredients']
    final_columns = ['id', 'name', 'first_brewed', 'abv', 'ibu', 'ph', 'principal_malt', 'ph_type', 'alcohol_type']
    
    df_p = pd.DataFrame(response.json())
    spk = ClientSpark(log=log)
    df = spk.whole_process(df=df_p, initial_columns=initial_columns, final_columns=final_columns)
    df_p = df.toPandas()
    if database:
        log.info('Using local Database')
        psql = ClientPSQL(log=log, table='beers', df=df_p )
        psql.inserting_rows()
    else:
        log.info('Using S3')
        json_df = df_p.to_json()
        clients3 = ClientS3(log=log, file_name='parsed.json', python='python2')
        clients3.upload_objects_to_s3(data=json_df)
