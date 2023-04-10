import pandas as pd
import numpy as np
import math

def sual_maker(rnd_eded):
    df=pd.read_csv('butun-suallar.csv')
    sual, sekil,cavab, sayilma_meyari, serh, menbe, muellif=df.loc[rnd_eded]
    data=np.array([sual, sekil, cavab, sayilma_meyari, serh, menbe, muellif])
    for i in range(7):
         if(data[i]=='nan'):
             data[i]=''
    sual,sekil, cavab, sayilma_meyari, serh, menbe, muellif =data
    return sual,sekil,'Cavab:'+cavab,'Sayılma meyarı:'+sayilma_meyari,'Şərh:'+serh,'Mənbə:'+menbe,'Müəllif:'+muellif

