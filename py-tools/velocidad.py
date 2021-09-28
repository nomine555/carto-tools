#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 16:18:39 2018

@author: fernando
"""

import pandas as pd
import numpy as np
import sys

if (len(sys.argv) != 1):
    print("demasiados parametros")
else:
    print("parametros incorrectos")

# Variables de entrada
input_file_map = "./mapa.txt";
output_file = "./script.sql";

# Parametros de cálculo
radius = 4;
minradius = 0.1;
minpoints = 5;

# Variables globales
earlymeets = 0;   

# Leemos el archivo con el mapa
tipos = {"X":np.float,"Y":np.float,"Z":np.float,"LAT":np.int32 }
df = pd.read_csv(input_file_map, sep='\s+', dtype=tipos, skiprows = {1}, skipfooter = 1)
#df = df.iloc[1:]
#df = df.iloc[:len(df)]


# Sacamos el ciclo y el numero de mapa
CL = df.CYCLE_LENGTH.median();
map_idx = df.MAP_IDX[2];

# definimos la función distancia entre dos puntos de una recta
def distancia_lineal(a,b):
    if (a > b):             
       return (a - b)
    else:
       return (b - a)

def distancia_LAT(a,b,CL):
    
    distancia = distancia_lineal(a,b);
    
    if (a > b):             
       distanciacl = distancia_lineal(a,b + CL)
    else:
       distanciacl = distancia_lineal(a + CL,b)
    
    if distanciacl > distancia:
        #print(str(a) + "," + str(b) + "=" + str(distancia))
        global earlymeets 
        earlymeets = earlymeets + 1;
        return distancia
    else: 
        return distanciacl

# Quitamos los puntos noLAT
n = len(df)
df = df[df.LAT != -10000]
print("Used points (LAT points): " + str(100*len(df)/n)+"%")

# Calculamos la velocidad de conducción con un algoritmo algo más complejo
# Usamos todos los punto en un cubo de Xmm
for index,row in df.iterrows():           
   lista_puntos = [];                          
   for index2,row2 in df.iterrows():     
       if index != index2:  
            if ((distancia_lineal(row['X'], row2['X']) < radius) and (distancia_lineal(row['Y'], row2['Y']) < radius) and (distancia_lineal(row['Z'], row2['Z']) < radius)):
                lista_puntos.append(index2);
   speed = [];
   N = 0;
   for index2 in lista_puntos:
       distancia = (((df.loc[index, 'X']- df.loc[index2, 'X'])**2 + (df.loc[index, 'Y']- df.loc[index2, 'Y'])**2 + (df.loc[index, 'Z']- df.loc[index2, 'Z'])**2)**(.5));
       tiempo =  distancia_LAT(df.loc[index, 'LAT'],df.loc[index2, 'LAT'], CL);
       if (tiempo > 0 and distancia > minradius):
           nspeed = distancia / tiempo;
           speed.append(nspeed);
   if (len(speed) > minpoints):
       speed.remove(min(speed));
       df.loc[index, 'IMPEDANCE'] = min(speed)*100;
   else:
       df.loc[index, 'IMPEDANCE'] = -10000;
   
    
# Exportamos a un archivo .sql
sql_sentence = "use Aces";
for index,row in df.iterrows():   
    sql_sentence = sql_sentence + "\nupdate points_table set impedance = " + str(df.loc[index,"IMPEDANCE"]) + "where map_idx = " + str(map_idx) + " and sequential_index = "+ str(df.loc[index,"POINT_IDX"]);
sql_sentence = sql_sentence + "\ngo";
print(sql_sentence,  file = open(output_file, 'w'))
