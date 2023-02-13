import pandas as pd
import re
import io



class ClientProcessing:
    def __init__(self, log:object):
        self.log = log


    def regex_cleaning(self, df:pd.DataFrame) -> pd.DataFrame:
        for column in df.columns:
            self.log.info(f' - ClientProcessing - regex_cleaning - Cleaning column : {column}')
            df[column] = df[column].str.replace("[^A-Za-z0-9@.]|^\\s+|\\s+$", '', regex=True)
        return df

    def filtering_and_column_accomodation(self, df:pd.DataFrame ) -> pd.DataFrame:
        df_filter = df[df['account_number'].str.contains('\D',regex=True)]
        df.loc[df_filter.index,'last_name']= df['last_name']+', '+df['account_number']
        df.loc[df_filter.index,'account_number']= df['email']
        df.loc[df_filter.index,'email']= df['extra']
        df_filter2 = df[df['email'].str.contains('\d+',regex=True,na=False)]
        df.loc[df_filter2.index,'account_number']= df['email']
        df.loc[df_filter2.index,'email']= df['extra']
        df = df.drop(0).reset_index(drop=True) 
        df.drop('extra',axis=1,inplace = True)
        return df

    def whole_processing(self,file:object, dataframe:bool=False, columns:list=['id','first_name','last_name','account_number','email','extra']) -> pd.DataFrame:
        self.log.info(f' - ClientProcessing - whole_processing - running whole_processing')
        data = re.sub('([\n])\D', "\t", file)
        data = io.StringIO(data)
        df = pd.read_csv(data, sep = "\t", encoding ='UTF-16LE', names=columns, skiprows =0)
        df = self.regex_cleaning(df=df)
        df = self.filtering_and_column_accomodation(df=df)
        if dataframe:
            return df
        else:
            csv_df = df.to_csv(index=False, sep='|')
            return csv_df
