import boto3
import json
import os
import sys

path = '/'.join(__file__.split('/')[:-2])

with open(f'{path}/utils/cred.json', 'r') as file:
    data = file.read()
    data = json.loads(data)

client = boto3.client('s3',
                      aws_access_key_id=data['aws_access_key_id'],
                      aws_secret_access_key=data['aws_secret_access_key']
                      )

class ClientS3:
    def __init__(self, log:object, bucket:str='name-of-bucket', nombre:str='Luciano', apellido:str='Argolo', file_name:str='parsed.csv', python:str=None):
        self.client = client
        self.BUCKET = bucket
        self.file_name = file_name
        self.nombre = nombre
        self.apellido = apellido
        self.log = log
        self.python = python

    def get_file(self, key:str='data/datos_data_engineer.tsv') -> str:
        self.log.info(f' - ClientS3 - get_file - getting file from path : {key}')
        return self.client.get_object(Bucket=self.BUCKET, Key=key)['Body'].read().decode('UTF-16LE')

    def upload_objects_to_s3(self, data:str) -> None:
        self.log.info(f' - ClientS3 - upload_object_to_s3 - uploading to path  : {self.nombre}-{self.apellido}/{self.python}/{self.file_name} in bucket: {self.BUCKET} ')
        with open(self.file_name, "w") as f:
            f.write(data)

        client.upload_file(self.file_name, self.BUCKET, f"{self.nombre}-{self.apellido}/{self.python}/{self.file_name}")
        os.remove(self.file_name)



