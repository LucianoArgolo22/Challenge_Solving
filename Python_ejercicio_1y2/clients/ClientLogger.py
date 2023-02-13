import logging

class ClientLogger:
    def __init__(self, filename:str, app_name:str) -> None:
        self.filename = filename
        self.level = logging.INFO
        self.format = f'[%(asctime)s] - %(process)d - %(levelname)s - %(message)s'
        self.app_name = app_name

    def config(self) -> None:
        logging.basicConfig(level=self.level, format=self.format,
                            handlers=[logging.FileHandler(self.filename),
                                logging.StreamHandler()])
                            
    def get_log(self) -> logging.Logger:
        self.config()
        return logging.getLogger(self.app_name)
