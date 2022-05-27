# https://stackoverflow.com/questions/50276202/tkinter-checkbutton-not-working

import os
from distutils.dir_util import copy_tree
import re
import subprocess
import configparser

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 

from mpl_toolkits.mplot3d.proj3d import proj_transform
from matplotlib.text import Annotation

from scipy.spatial.distance import cdist
from scipy.sparse.csgraph import shortest_path
import sklearn.cluster as cluster

import scipy.stats as st
from tkinter import Tk
from tkinter import messagebox

import configparser
from my_dialogs import zoneDialog

# returns confidence interval of mean
def confIntMean(a, conf=0.95):
  mean, sem, m = np.mean(a), st.sem(a), st.t.ppf((1+conf)/2., len(a)-1)
  return mean - m*sem, mean + m*sem


# Funciones para ver etiquetas en 3D
#############################################
class Annotation3D(Annotation):
    '''Annotate the point xyz with text s'''

    def __init__(self, s, xyz, *args, **kwargs):
        Annotation.__init__(self,s, xy=(0,0), *args, **kwargs)
        self._verts3d = xyz        

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj_transform(xs3d, ys3d, zs3d, self.axes.M)
        self.xy=(xs,ys)
        Annotation.draw(self, renderer)
        
def annotate3D(ax, s, *args, **kwargs):
    '''add anotation text s to to Axes3d ax'''

    tag = Annotation3D(s, *args, **kwargs)
    ax.add_artist(tag)       
        
# Funciones auxiliares #
########################

def get_path(Pr, i, j):
    path = [j]
    k = j
    while Pr[i, k] != -9999:
        path.append(Pr[i, k])
        k = Pr[i, k]
    return path[::-1]


def f(x): 
    if (x > 6.5):
        return np.inf
    elif (x < 2):
        return 0.00000000001
    else:
        return (x**50)

def g(x): 
    if (x > 8):
        return np.inf
    elif (x < 2):
        return 0.00000000001
    else:
        return (x**50)

def h(x): 
    if (x > 14):
        return np.inf
    elif (x < 2):
        return 0.00000000001
    else:
        return (x**50)


# Función que busca el trayecto utiliza las variables globales.
# Trabaj sobre el dataframe dfn
     
def trayecto(zona, dfn, intento):
    
    global color, distancias
    
    fdist = 0
    
    # Lo intentamos con 3 funciones diferentes de distancia
    while (fdist <= 3): 
    #if(True):
        dfn.loc[dfn['Site'] == zona, 'Seq'] = np.NaN
        dfn.loc[dfn['Site'] == zona, 'Distancia'] = np.NaN
        
        # Cogemos la zona, y una matriz X, Y, Z        
        dfz = dfn[dfn['Site'] == zona]        
        puntos = dfz[['X','Y','Z']];   
        if(len(puntos) < 2):
            return
    
        #dfn['Color'] = 1; 
        
        # Calculamos la distancia de todos con todos
        distancias = cdist(puntos, puntos);     
        distancias_ord = np.sort(distancias.flatten())
     
        
        # En el primer intento cogemos los dos puntos más alejados
        # En los siguienes nos vamos desplazando hasta que haya un error
        if (intento == 0):
            m,mm = np.where(distancias >= np.amax(distancias))    
            inicio = m[0]
            fin    = m[1]          
        else:
            if (aleatorio): 
                print("Algoritmo Aleatorio")
                alea  = distancias.shape[0]
                inicio = np.random.randint(low=0, high=alea, size=(1,))[0]
                fin    = np.random.randint(low=0, high=alea, size=(1,))[0]                           
            else:
                maximo = intento*np.amax(distancias)/6 + np.amax(distancias)/3
                distancias_ord = distancias_ord[distancias_ord > maximo]
                try:
                    m,mm = np.where(distancias == distancias_ord[0])    
                except:                
                    return False
                inicio = m[0]
                fin    = m[1]          
    
        # Utilizamos una de las 3 funciones distancia f, q, h. 
        # Elevan a un número muy grande la distancia para evitar pasar por puntos intermedios
        # Consideran la distancia infinita a partir de un valor. 
    
        if (fdist % 3 == 0):           
            distancias = np.vectorize(h)(distancias)   
        elif(fdist % 3 == 1): 
            distancias = np.vectorize(g)(distancias)  
        else:
            distancias = np.vectorize(f)(distancias)            
    
        # Buscamos el camino más corto    
        dist_matrix, predecessors = shortest_path(csgraph=distancias, directed=True, return_predecessors = True, method = 'FW')  
        camino = get_path(predecessors, inicio, fin);
        color = color + 1

        # Asignamos el valor de la secuencia del camino. 
        n = 1;
        for index in camino:  
            dfn.loc[dfn['SiteIndex'] == dfz.iloc[index,2], ['Seq']] = n;   
            dfn.loc[dfn['SiteIndex'] == dfz.iloc[index,2], ['Color']] = color;                  
            n = n + 1;
        n = n - 1;
 
        # Ahora buscamos el camino de vuelta circular
        # Borramos todos los puntos que hemos recorrido e intentamos volver al inicio 
        dfz = dfn[dfn['Site'] == zona]
    
        for index, row in dfz.iterrows():
            if ( (row['Seq'] > 1) and (row['Seq'] < n ) ):
                dfz = dfz.drop(index)
                
        # Cogemos el inicio y el fin para el camino de vuelta
        p = -1
        for index, row in dfz.iterrows():
            p = p + 1     
            if (row['Seq'] == 1):
                inicio = p       
            if (row['Seq'] == n):
                fin = p                

        # Calculamos distancias de nuevo 
        puntos =  dfz[['X','Y','Z']];   
        distancias = cdist(puntos, puntos);
    
        # Utilizamos de nuevo las funciones f, q, h
        if (aleatorio):
            distancias = np.vectorize(h)(distancias) 
        else:
            if (fdist % 3 == 0):           
                distancias = np.vectorize(h)(distancias) 
            elif(fdist % 3 == 1): 
                distancias = np.vectorize(g)(distancias)    
            else:
                distancias = np.vectorize(f)(distancias)     
    
        # Calculamos el camino
        dist_matrix, predecessors = shortest_path(csgraph=distancias, directed=True, return_predecessors = True, method = 'FW') 
        camino2 = get_path(predecessors, fin, inicio);
    
        # Asignamos la secuencia
        color = color + 1
        if (len(camino2) > 1):            
            for index in camino2:  
                dfn.loc[dfn['SiteIndex'] == dfz.iloc[index,2], ['Seq']] = n;
                dfn.loc[dfn['SiteIndex'] == dfz.iloc[index,2], ['Color']] = color;              
                n = n + 1; 
                fdist = 10;
        else:
            # Como no logramos camino circular, lo volvemos a intentar con la siguiente función distancia. 
            fdist = fdist + 1;
            
    # Retunr True, mientras se pueda realizar otro cálculo
    return True
    
def segmenta(dfn, N):
    
    global labels,color
    
    elementos = dfn['Comment'].value_counts().index.tolist();  

    if ((N == 0) and (len(elementos) > 1)):
    
        # Creamos las secciones en función de los comentarios y ponemos un color
        ultimo = "any"
       
        for index, row in dfn.iterrows():   
            if (pd.isnull(row['Comment'])):
                dfn.at[index,'Site'] = ultimo
                dfn.at[index,'Color'] = color
            elif (ultimo == row['Comment'].split('-')[0]):
                dfn.at[index,'Color'] = color
                dfn.at[index,'Site'] = ultimo
            elif (row['Comment'] == 'o'):
                dfn.at[index,'Color'] = 1
                dfn.at[index,'Site'] = 'o'
            else:
                ultimo = row['Comment'].split('-')[0]
                color = color + 1
                dfn.at[index,'Site'] = ultimo
                dfn.at[index,'Color'] = color
    else:
        # CLUSTERING   
        X = dfn[['X','Y','Z']].to_numpy();        
        kmeans = cluster.KMeans(n_clusters=N)
        kmeans = kmeans.fit(X)
        labels = kmeans.labels_
        for index, row in dfn.iterrows(): 
            dfn.at[index,'Site']  = "z" + str(labels[index])
            dfn.at[index,'Color'] = labels[index]
          
    return dfn

def procesa(dir_paciente, dfResumen, dfTotal, dfRfs, dflistado):
    
    global dfx, color;         
    color = 1
                 
 # Cargamos los datos
           
    input_file   = dir_paciente + "\\Sites.txt";
    input_file2  = dir_paciente + "\\VisiTagSessions.txt";    
    output_file   = dir_paciente + '\\..\\' + os.path.basename(os.path.dirname(input_file)) + '.csv';
    output_file2  = dir_paciente + '\\..\\' + os.path.basename(os.path.dirname(input_file)) + '.txt';    

    print("#######################################################")
    print("Procesando Archivo:")
    print(input_file)
    
    try:
        #df  = pd.read_csv(input_file, sep='\s+', index_col=0, engine='python')
        #df2 = pd.read_csv(input_file2, sep='\s+', index_col=0, engine='python')
        df  = pd.read_fwf(input_file, index_col=0, widths=[20,20,20,20,20,20,20,20,20,20,20,20,20,20,20], engine='python')
        df2 = pd.read_fwf(input_file2, index_col=0,widths=[20,20,20,20,20,20], engine='python')

        dfn = df.join(df2)
        dfn.reset_index(level=0, inplace=True)
        del df
        del df2
    except Exception as e:
        print('Error leyendo archivo: ' + input_file)
        print(e)
        return dfResumen, dfTotal, dfRfs, dflistado
       
    if (confirm):
        nsegmentos = int(segmentos)
        
        while (True):
            try:
                dfn = segmenta(dfn,nsegmentos)
                # Mostramos las secciones. 
                try:
                    plt.close()   
                except Exception as e:
                    print(e)                                   
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
                ax.set_title("All points " + dir_paciente )
                ax.scatter(dfn['X'].to_numpy(),dfn['Y'].to_numpy(),dfn['Z'].to_numpy(), c = dfn['Color'].to_numpy())
                plt.draw()
                plt.pause(1)
                
            except Exception as e: 
                print("Error con la segmentación Automática")
                print(e)
                dflistado = dflistado.append({'directorio' : input_file, 'procesado' : 'No'}, ignore_index=True)
                plt.close()
                return dfResumen, dfTotal, dfRfs, dflistado            
            
            question = messagebox.askyesnocancel(
                  title="¿Aceptar Segmentación?",
                  message="Si - Aceptar \nNo - Reintentar con más segmentos \nCancelar - Descartar",
                  default=messagebox.YES)
                       
            if question:
                break;
            elif question is None:
                dflistado = dflistado.append({'directorio' : input_file, 'procesado' : 'No'}, ignore_index=True)
                plt.close()
                return dfResumen, dfTotal, dfRfs, dflistado 
            else:
                nsegmentos = nsegmentos + 1;
                if (nsegmentos > 5):
                    nsegmentos = 1
    else:
        try:
            dfn = segmenta(dfn,int(segmentos))
        except:
            print("Error con la segmentación Automática")
            dflistado = dflistado.append({'directorio' : input_file, 'procesado' : 'No'}, ignore_index=True)
            return dfResumen, dfTotal, dfRfs, dflistado            
    
    plt.close()
    visitags_totales = len(dfn.index)
    print("Visitags: ",visitags_totales)
    
    # Descartamos los elementos con errores
    if (not FTI):
        dfn = dfn[dfn['RFIndex'] > 0]
        dfn = dfn[dfn['ImpedanceDrop'] > 0]
        dfn = dfn[dfn['MaxTemperature'] > 0]
        dfn = dfn[dfn['MaxPower'] > 0]
        
    # Contamos Visitags totales
    visitags_totales = len(dfn.index)
    print("Visitags Utilizables: ",visitags_totales)

    # Contamos Visitags que cumplen tagindex
    dfnd = dfn[dfn['RFIndex'] > int(tagindex)]    
    visitags_cumplen = len(dfnd.index)
    print("Visitags Cumplen: ",visitags_cumplen)

    
    # Descartamos los elementos por Ablation Index
    if (not FTI):
        dfn = dfn[dfn['RFIndex'] > int(tagindexd)]
    else:
        dfn = dfn[dfn['FTI'] > int(tagindexd)]    
    
    # Miramos cuantas secciones hay
    elementos = dfn['Site'].value_counts().index.tolist();
    
    # Ejecutamos el algoritmo en cada zona
    intento = 0
    while (True):
                  
        No_revisar = True
        for zona in elementos:   
            revisar = trayecto(zona,dfn,intento);
            No_revisar = No_revisar and revisar;

        # Calculamos las Distancias
        try:
            for index, row in dfn.iterrows():    
                p1 = dfn.loc[(dfn['Seq'] == row['Seq'])     & (dfn['Site'] == row['Site']), ['X','Y','Z']]
                p2 = dfn.loc[(dfn['Seq'] == row['Seq'] + 1) & (dfn['Site'] == row['Site']), ['X','Y','Z']]
                d = cdist(p1,p2)            
                if (d.size > 0):
                    dfn.loc[(dfn['Seq'] == row['Seq']) & (dfn['Site'] == row['Site']), ['Distancia']] = d[0][0]          
        except:
            print("Error calculando trayecto")
            dflistado = dflistado.append({'directorio' : input_file, 'procesado' : 'No'}, ignore_index=True)
            return dfResumen, dfTotal, dfRfs, dflistado
    
        # Mostramos los datos    
        for zona in elementos:           
            dfx = dfn[dfn['Site'] == zona]
            
            print()
            print(zona)
            print('---------')
            print('Distancia Media ', dfx['Distancia'].mean()) 
            print('Distancia maxima ',dfx['Distancia'].max()) 
            #print('Max Gap:', dfx.loc[dfx['Distancia'] == dfx['Distancia'].max(),'Seq']  )          
            

        # Dibujamos los trayectos    
        if (confirm2):        
            try:
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
                ax.set_title(dir_paciente.replace("..\\","") )
                for zona in elementos:  
                    dfp = dfn[dfn['Site'] == zona]              
                    ax.scatter(dfp['X'].to_numpy(),dfp['Y'].to_numpy(),dfp['Z'].to_numpy(), label = zona)
        
                ax.legend()    
                xyzn = zip(dfn['X'].to_numpy(),dfn['Y'].to_numpy(),dfn['Z'].to_numpy())
                labels = dfn['Seq'].to_numpy()

                for j, xyz_ in enumerate(xyzn): 
                    annotate3D(ax, s = str(labels[j]), xyz=xyz_, fontsize=10, xytext=(-3,3),
                               textcoords='offset points', ha='right',va='bottom')        
                plt.draw()
                plt.pause(1)
            except:
                print("Cannot plot nothing!")
                dflistado = dflistado.append({'directorio' : input_file, 'procesado' : 'No'}, ignore_index=True)
                return dfResumen, dfTotal, dfRfs, dflistado
        
        # Zonas en las que hay datos    
        zonas = [False,False,False,False, False]
        for zona in elementos:                           
            zonas[int(zona.replace('z',''))] = True;
            
        if (confirm2):                   
            inputDialog = zoneDialog(root, "¿Aceptar Secuencia de tags?",zonas)
            root.wait_window(inputDialog.top)
            question = inputDialog.checkresult;
            zonas_seleccionadas = [inputDialog.cvar1.get(), inputDialog.cvar2.get(), inputDialog.cvar3.get(), inputDialog.cvar4.get(), inputDialog.cvar5.get()]                       
            print('zonas seleccionadas: ', zonas_seleccionadas)
        else:
            question = True;
            zonas_seleccionadas = zonas;

        # Si decidimos procesar esa linea
        if question:
            plt.close()
            break
        elif question is None:    
            dflistado = dflistado.append({'directorio' : input_file, 'procesado' : 'R'}, ignore_index=True)
            copy_tree(dir_paciente, dstdir +  "\\revision\\" + os.path.basename(os.path.normpath(dir_paciente)))
            plt.close()
            print("Marcado para revisión")
            return dfResumen, dfTotal, dfRfs, dflistado       
        else:
            if(not No_revisar):
                print("No es posible segmentarlo de otra forma, guardado para revisión")
                dflistado = dflistado.append({'directorio' : input_file, 'procesado' : 'No'}, ignore_index=True)            
                copy_tree(dir_paciente, dstdir +  "\\revision\\" + os.path.basename(os.path.normpath(dir_paciente)))
                return dfResumen, dfTotal, dfRfs, dflistado 
                break
            plt.close()            
            intento = intento + 1
            
  
    if ('Distancia' in dfn.columns):
        
        dflistado = dflistado.append({'directorio' : input_file, 'procesado' : 'Si'}, ignore_index=True)    
       
        # Calculamos el resumen de datos
        for zona in elementos:                       
            
            dfx = dfn[dfn['Site'] == zona]
            
            visitags_secuencia    = dfx[dfx.Seq > 0].shape[0]
            visitags_gaps_55      = dfx[dfx.Distancia > 5.5].shape[0]
            visitags_gaps_6       = dfx[dfx.Distancia > 6].shape[0]
            visitags_gaps_65      = dfx[dfx.Distancia > 6.5].shape[0]
            visitags_totales_zona = len(dfx.index)
            # Contamos los que cumplen en zona
            dfxd = dfx[dfx['RFIndex'] > int(tagindex)]
            visitags_cumplen_zona = len(dfxd.index)
                
            # Intervalos de confianza          
            try:
                dfmm =  dfx[dfx["Distancia"] > 0]
                data = dfmm["Distancia"].to_numpy()
                intervalo99 = confIntMean(data, conf=0.99)
                intervalo95 = confIntMean(data, conf=0.95)
                intervalo90 = confIntMean(data, conf=0.90)
            except:
                print('Error con los intervalos de confianza')         
                                    
            newline = {'file': input_file.replace(rootdir,"").replace("Sites.txt",""),
                       'zona': zona,
                       'Distancia Media ':    dfx['Distancia'].mean(),
                       'Distancia Mediana ':  dfx['Distancia'].median(),
                       'Desviacion estandar ':dfx['Distancia'].std(),
                       'Distancia maxima ':   dfx['Distancia'].max(), 
                       '# Visitags': visitags_totales,         
                       '# Visitags >300' : visitags_cumplen,  
                       '# Visitags en Zona': visitags_totales_zona, 
                       '# Visitags en Zona >300' : visitags_cumplen_zona,                       
                       '# Visitags en Zona y linea': visitags_secuencia,
                       '# Gaps >5,5': visitags_gaps_55,
                       '# Gaps >6': visitags_gaps_6,
                       '# Gaps >6,5': visitags_gaps_65,
                       '# 99%': intervalo99, 
                       '# 95%': intervalo95, 
                       '# 90%': intervalo90,
                       'DurationTime mean': dfx['DurationTime'].mean(),
                       'DurationTime STD': dfx['DurationTime'].std(),
                       'AverageForce mean':dfx['AverageForce'].mean(),
                       'AverageForce STD':dfx['AverageForce'].std(),
                       'MaxTemperature mean':dfx['MaxTemperature'].mean(),
                       'MaxTemperature STD':dfx['MaxTemperature'].std(),
                       'MaxPower mean':dfx['MaxPower'].mean(),
                       'MaxPower STD':dfx['MaxPower'].std(),
                       'BaseImpedance mean':dfx['BaseImpedance'].mean(),
                       'BaseImpedance STD':dfx['BaseImpedance'].std(),
                       'ImpedanceDrop mean':dfx['ImpedanceDrop'].mean(),
                       'ImpedanceDrop STD':dfx['ImpedanceDrop'].std(),
                       'RFIndex mean':dfx['RFIndex'].mean(),
                       'RFIndex STD':dfx['RFIndex'].std()                       
                       }
            
            if ((dfx['Distancia'].std() > 0) and zonas_seleccionadas[int(zona.replace('z',''))]):
                dfResumen  = dfResumen.append(newline, ignore_index=True)        
            '''
            if ((zona.upper() == "DER") or (zona.upper() == "IZQ") or (zona == "z0") or (zona == "z1") ):               
                col = dir_paciente.replace(rootdir,"") + "_" + zona.upper()
                columna = dfx['Distancia'].dropna().reset_index(drop=True)
                dfTotal = pd.concat([dfTotal, columna], axis=1)   
                dfTotal.columns = [*dfTotal.columns[:-1], col]
            '''
    else:        
        print("Error calculando trayecto")
        dflistado = dflistado.append({'directorio' : input_file, 'procesado' : 'No'}, ignore_index=True)
        return dfResumen, dfTotal, dfRfs, dflistado      
                        
    # Exportamos a csv.
    dfRfs = pd.concat([dfRfs, dfn])
    dfn.to_csv(output_file,sep = ';', decimal=',');
    return dfResumen, dfTotal, dfRfs, dflistado

def leer_configuracion():
    
    global rootdir, dstdir, tagindex, tagindexd, Study_Name, segmentos, sql_file, confirm, confirm2, procesar, FTI, resumefile, alldatafile,allrfsfile, procesfiles, subdir, datadir, mapsdir, patientdata,aleatorio;
    
    config = configparser.ConfigParser()
    config.read('visitag.ini')
    rootdir      = config['DEFAULT']['Carpeta_Origen']
    dstdir       = config['DEFAULT']['Carpeta_Destino']
    tagindex     = config['DEFAULT']['Ablation_Index']
    tagindexd    = config['DEFAULT']['Ablation_Index_Discard']
    Study_Name   = config['DEFAULT']['Study_Name']
    segmentos    = config['DEFAULT']['Segmentos']
    sql_file     = config['DEFAULT']['Archivo_SQL']

    if (config['DEFAULT']['Confirmar'] == "Si"):
        confirm      = True;
    else: 
        confirm      = False;
        
    if (config['DEFAULT']['Aleatorio'] == "Si"):
        aleatorio      = True;
    else: 
        aleatorio      = False;
        
    if (config['DEFAULT']['Confirmar2'] == "Si"):
        confirm2      = True;
    else: 
        confirm2      = False;        
    
    if (config['DEFAULT']['Solo_cargar_datos'] == "Si"):
        procesar     = False;
    else: 
        procesar      = True;    

    if (config['DEFAULT']['Usar FTI'] == "Si"):
        FTI     = True;
    else: 
        FTI     = False;    

    if (config['DEFAULT']['Cargar_desde_Carto'] == "Si"):
        rootdir      = "F:\\CartoData\\Patients\\"
        
    # Variables Globales
    resumefile   = dstdir + "per-tag-statics.csv"
    alldatafile  = dstdir + "alldata.csv"
    allrfsfile   = dstdir + "allrfs.csv"
    procesfiles  = dstdir + "procesed.csv"
    subdir       = '\\Studies\\'
    datadir      = '\\RawData\\'
    mapsdir      = '\\Maps\\'
    patientdata  = '\\Label.INI'
    
#############################################################################
# INICIO DE PROGRAMA
#############################################################################

root = Tk()
root.withdraw()
lista_pacientes = [];
dflistado = pd.DataFrame([], columns = ['directorio','procesado'])

leer_configuracion()

# Directorios de trabajo
print("")
print("#######################################################")
print("")
print("Directorio Origen:  " + rootdir)
print("Directorio Destino: " + dstdir)

try:
    if(not os.path.isdir(dstdir)):                                            
        os.mkdir(dstdir)
except:
    print('Error Creando directorio')             
                            
# Cargamos los datos del Carto, o de una carpeta
if (rootdir      == "F:\\CartoData\\Patients\\"):
    print("Accediendo a los directorios de Carto")
    for paciente in os.listdir(rootdir):
        item = os.path.join(rootdir, paciente)        
        if (not os.path.isfile(item) and re.match('Patient(.*)', paciente)):        
            for estudio in os.listdir(rootdir + paciente + subdir):    
                item = rootdir + paciente + subdir + estudio + datadir;           
                mapd  = rootdir + paciente + subdir + estudio + mapsdir;                            
                if os.path.isdir(item):                                                                
                    for zipfile in os.listdir(item):
                        print(zipfile)
                        try:
                            found = re.search('Export_(.*)-(.*)-(.*)-(.*)-(.*)\\.zip$', zipfile)    
                            if (re.match(Study_Name, found[1])):
                                cf  = pd.read_csv(mapd + os.listdir(mapd)[0] + patientdata, sep='=')                   
                                finaldir = cf.iloc[2,1].strip() + '-' + cf.iloc[4,1].strip()
                                item = rootdir + paciente + subdir + estudio + datadir + zipfile;
                                try:
                                    if(not os.path.isdir(dstdir + finaldir)):                                            
                                        os.mkdir(dstdir + finaldir)
                                    lista_pacientes.append(dstdir + finaldir)
                                    # dflistado = dflistado.append({'directorio' : finaldir}, ignore_index=True)
                                    
                                except:
                                    print('Error Creando directorio')                        
                                try:
                                    cmd = ['7z', 'e', '-y', '-o' + dstdir + finaldir, item, 'VisitagExport\Sites.txt', 'VisitagExport\VisiTagSessions.txt']                                                                                                
                                    sp = subprocess.run(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)                                                                     
                                    #copyfile(mapd + os.listdir(mapd)[0] + patientdata, dstdir + finaldir + patientdata)
                                except:
                                    print('Error descomprimiendo')                        
                        except:
                            print('Error con la carpeta')                                                            
else: 
    for paciente in os.listdir(rootdir):
        item = os.path.join(rootdir, paciente)        
        lista_pacientes.append(item)                                                                            
        
# Procesamos los datos
if (procesar):
    print("Procesando visitags...")
    print("")                                 
    # Data Frame resumen
    dfResumen = pd.DataFrame([], columns = ['file','zona','Distancia Media ',
                                            'Distancia Mediana ','Desviacion estandar ','Distancia maxima ',
                                            '# Visitags','# Visitags >300',
                                            '# Visitags en Zona','# Visitags en Zona >300', '# Visitags en Zona y linea',
                                            '# Gaps >5,5', '# Gaps >6','# Gaps >6,5',
                                            '# 99%', '# 95%','# 90%'
                                            'DurationTime mean','DurationTime STD','AverageForce mean',
                                            'AverageForce STD','MaxTemperature mean','MaxTemperature STD',
                                            'MaxPower mean','MaxPower STD','BaseImpedance mean',
                                            'BaseImpedance STD','ImpedanceDrop mean','ImpedanceDrop STD',
                                            'RFIndex mean','RFIndex STD'])
                      
    dfTotal = pd.DataFrame([], columns = [])                                       
    dfRfs   = pd.DataFrame([], columns = [])  

    for dir_paciente in lista_pacientes:
        if (os.path.isfile(dir_paciente + '\\Sites.txt')):
            dfResumen, dfTotal, dfRfs, dflistado = procesa(dir_paciente, dfResumen, dfTotal, dfRfs, dflistado)
            # Exportamos los datos            
            dfTotal.to_csv(alldatafile, sep = ';', decimal=',');
            dfRfs.to_csv(allrfsfile, sep = ';', decimal=',');
            dflistado.to_csv(procesfiles, sep = ';', decimal=',');
            dfResumen ['file'] = dfResumen['file'].str.replace('\\','')
            dfResumen.to_csv(resumefile, sep = ';', decimal=',');

'''        
# Tenemos archivo SQL
if(len(sql_file.strip())>0):
    dfsql  = pd.read_fwf(rootdir + "\\" + sql_file, index_col=0,infer_nrows=2,skipfooter=2, engine='python')
    dfsql = dfsql.drop(index='-------')
    
    # Esto es exclusivo de un problema que tuve con los Estudios de Navarra que cambie el nombre en la BD. 
    dfsql ['StudyName'] = dfsql['StudyName'].str.replace('_FA','FA')
    dfsql ['StudyName'] = dfsql['StudyName'].str.replace('_AFIB','AFIB')
    dfsql ['StudyName'] = dfsql['StudyName'].str.replace('FAx3','FA')
    dfsql ['StudyName'] = dfsql['StudyName'].str.replace('RedoFA','Redo_FA')
    dfsql ['StudyName'] = dfsql['StudyName'].str.replace('_Study 2','Study 2')
    
    dfsql["ID"] = dfsql['NUMHIST'] + "-" + dfsql["StudyName"]

    dfTT = dfsql.merge(dfResumen,left_on='ID',right_on='file',how='right')
    dfTT.to_csv(resumefile, sep = ';', decimal=',');
    dfsql.to_csv(resumefile+"-sql.csv", sep = ';', decimal=',');

'''
    
## Funciones no utilizadas para el futuro. 
'''
    # Buscamos un punto inicial en los comentarios
    inicio = -1
    n = 0
    for index, row in dfz.iterrows():
        if ( not pd.isnull(row['Comment']) and len(row['Comment'].split('-')) > 1):
            if (row['Comment'].split('-')[1] == 'inicio'):
                inicio = n;                
            if (row['Comment'].split('-')[1] == 'fin'):
                fin = n;
        n = n + 1
      

    # Si no hay punto inicial cogemos los dos puntos mas alejados. 
    if (inicio == -1):
''' 
    
