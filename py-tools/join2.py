import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

file1   = '..\..\Estudios\Estudios-Navarra-last-proccessed-1\per-tag-statics.csv'
file2   = '..\..\Estudios\Estudios-Navarra-last-proccessed-2\per-tag-statics.csv'
file3   = '..\..\Estudios\Estudios-Navarra-last-proccessed-3\per-tag-statics.csv'
file4   = '..\..\Estudios\Estudios-Navarra-last-proccessed-4\per-tag-statics.csv'
file5   = '..\..\Estudios\Estudios-Navarra-last-proccessed-5\per-tag-statics.csv'
file6   = '..\..\Estudios\Estudios-Navarra-Revisar-1\per-tag-statics.csv'
file7   = '..\..\Estudios\Estudios-Navarra-Revisar-1\per-tag-statics-1.csv'
file8   = '..\..\Estudios\Estudios-Navarra-Revisar-1\per-tag-statics-2.csv'

sql_file =       "..\..\Estudios\Estudios-Navarra-Revisar-1\\03-23-2022-21-47-30-66-cartotimes.txt"
fileout  =       '..\..\Estudios\Estudios-Navarra-Revisar-1\join.csv'
patientsfile  =  '..\..\Estudios\Estudios-Navarra-Revisar-1\listado-total.xls'

print(sql_file)
# Cargamos los archivos de Visitags
df   = pd.read_csv(file1, sep = ';', decimal=',',index_col=0, engine='python')
df2  = pd.read_csv(file2, sep = ';', decimal=',',index_col=0, engine='python')
df3  = pd.read_csv(file3, sep = ';', decimal=',',index_col=0, engine='python')
df4  = pd.read_csv(file4, sep = ';', decimal=',',index_col=0, engine='python')
df5  = pd.read_csv(file5, sep = ';', decimal=',',index_col=0, engine='python')
df6  = pd.read_csv(file6, sep = ';', decimal=',',index_col=0, engine='python')
df7  = pd.read_csv(file7, sep = ';', decimal=',',index_col=0, engine='python')
df8  = pd.read_csv(file8, sep = ';', decimal=',',index_col=0, engine='python')

dft = pd.concat([df,df2,df3,df4,df5,df6,df7,df8])

# Agrupamos por zonas
dg  = dft.groupby(["file","# Visitags","# Visitags >300"])[["Distancia Media ","Desviacion estandar ","DurationTime STD","AverageForce mean","AverageForce STD","MaxTemperature mean","MaxTemperature STD","MaxPower mean","BaseImpedance mean","BaseImpedance STD","ImpedanceDrop mean","ImpedanceDrop STD","RFIndex mean","RFIndex STD","DurationTime mean"]].agg(["mean"])
dg2  = dft.groupby(["file"])[["Distancia maxima ","MaxPower STD"]].agg(["max"])
dg3  = dft.groupby(["file"])[["# Visitags en Zona y linea","# Gaps >5,5","# Gaps >6","# Gaps >6,5"]].agg(["sum"])

dg = dg.merge(dg2,left_on='file',right_on='file',how='left')
dg = dg.merge(dg3,left_on='file',right_on='file',how='left')
dg.columns = [' '.join(col).strip() for col in dg.columns.values]

# Cargamos el archivo de la BD del Carto
dfsql  = pd.read_fwf(sql_file, index_col=0,infer_nrows=2,skipfooter=2, engine='python')
dfsql = dfsql.drop(index='-------')
    
# Esto es exclusivo de un problema que tuve con los Estudios de Navarra que cambie el nombre en la BD. 
dfsql ['StudyName'] = dfsql['StudyName'].str.replace('_FA','FA')
dfsql ['StudyName'] = dfsql['StudyName'].str.replace('_AFIB','AFIB')
dfsql ['StudyName'] = dfsql['StudyName'].str.replace('FAx3','FA')
dfsql ['StudyName'] = dfsql['StudyName'].str.replace('RedoFA','Redo_FA')
dfsql ['StudyName'] = dfsql['StudyName'].str.replace('_Study 2','Study 2')
dfsql["ID"] = dfsql['NUMHIST'] + "-" + dfsql["StudyName"]

# Juntamos los datos del Carto
dftt = dfsql.merge(dg,left_on='ID',right_on='file',how='right')
dftt = dftt.dropna(subset=['NUMHIST'])
dftt['NUMHIST'] = dftt['NUMHIST'].astype(int)
dftt['Date2'] = pd.to_datetime(dftt['Date']).dt.date
#dftt.columns = dftt.columns.str.replace('\'','')

# Cargamos los datos de paciente del Excel
dfp = pd.read_excel(patientsfile)
dfp['Date3'] = pd.to_datetime(dfp['FechaFA']).dt.date
dfp["Recidiva"] = dfp["ReciAño"].str.replace('(','0')
dfp["Recidiva"] = pd.to_numeric(dfp["ReciAño"], errors='coerce')


# Solo primeros procedimientos
dfX = dftt.merge(dfp, left_on='NUMHIST', right_on='NHC', how='left')
dfD = dfX[ (dfX['Date2'].eq(dfX['Date3'])) ]

# Guardamos el archivo total
dfD.drop_duplicates().to_csv(fileout, sep = ';', decimal=',');

# Plot

#plt.scatter(dfD["Recidiva"].to_numpy(), dfD["# Gaps >6,5 sum"].to_numpy(), s = 1 )
plt.scatter(dfD["Recidiva"].to_numpy(), dfD["Distancia maxima  max"].to_numpy(), s = 1 )
plt.show()
