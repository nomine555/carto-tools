import numpy as np
import pandas as pd

processedfile = '..\..\Estudios\Estudios-Navarra-Analisis\per-tag-statics.csv'
patientsfile  = '..\..\Estudios\Estudios-Navarra-Analisis\listado-total.xls'
fileout       = '..\..\Estudios\Estudios-Navarra-Analisis\join.csv'


df  = pd.read_csv(processedfile, sep = ';', decimal=',',index_col=0, engine='python')
df2 = pd.read_excel(patientsfile)

df = df.dropna(subset=['NUMHIST'])
df['NUMHIST'] = df['NUMHIST'].astype(int)
df2['Date'] = pd.to_datetime(df2['FechaFA']).dt.date

dfP = df.merge(df2, left_on='NUMHIST', right_on='NHC', how='left')
print(df['NUMHIST'].value_counts())

dfP.to_csv(fileout, sep = ';', decimal=',');
