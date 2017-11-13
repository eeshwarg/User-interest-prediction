import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

def readFile(filepath):
    df = pd.read_csv(filepath, sep='\t')
    df['Query'] = df['Query'].astype(str)
    df['QueryTime'] = pd.to_datetime(df['QueryTime'])
    # df['ItemRank']=df['ItemRank'].astype(int)
    del df['ClickURL']
    # print df.dtypes
    # print df.head()
    return df

def readDataset(folderpath):
    filePrefix = "user-ct-test-collection-"
    dfList = []
    for i in xrange(1,11):
        numeral = str(i)
        if i != 10:
            numeral = '0' + numeral
        filename = filePrefix + numeral + '.txt'
        filepath = folderpath + filename
        file_dataframe = readFile(filepath)
        dfList.append(file_dataframe)

    ds = pd.concat(dfList)
    return ds



if __name__ == '__main__':
    # folderpath = '../Dataset/'
    # ds = readDataset(folderpath)
    # print ds.describe()
    filepath = '../Dataset/user-ct-test-collection-01.txt'
    ds = readFile(filepath)
    timeHistogram(ds)
    # averageItemRank(ds)
