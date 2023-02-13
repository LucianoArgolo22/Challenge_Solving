
#%%
from clients.ClientS3 import ClientS3
from clients.ClientProcessing import ClientProcessing
from clients.ClientLogger import ClientLogger
from clients.ClientSesPSQL import ClientPSQL
import sys

if __name__ == "__main__":
    logger = ClientLogger(filename='parser_s3.log', app_name='parser_s3')
    log = logger.get_log()

    log.info(f'Arguments inserted: {sys.argv}')
    database = True if len(sys.argv) == 2 and sys.argv[1] == 'True'  else False
    clients3 = ClientS3(log=log, python='python1')
    file = clients3.get_file()
    process = ClientProcessing(log=log)
    
    if database:
        log.info('Using local Database')
        df = process.whole_processing(file=file, dataframe=True)
        psql = ClientPSQL(log=log, table='users', df=df )
        psql.inserting_rows()

    else:
        log.info('Using S3')
        csv_df = process.whole_processing(file=file, dataframe=False)
        clients3.upload_objects_to_s3(data=csv_df)

