#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 16:18:39 2018

@author: fernando
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Variables de entrada
input_file_map = "./mapascarto/4-1-Flutter_car.txt";
map_idx = 6;
CL = 270;


# Variables globales
nombre_columnas = ['id','type','point_id','map_id','x','y','z','a','b','g','bipolar','unipolar','LAT','Imp','del'];
usa_columnas = ['point_id','x','y','z','a','b','g','unipolar','bipolar','LAT','Imp','del'];
output_file = "script.sql";
radius = 3;
minradius = 0.1;
minpoints = 6;
maxspeed = 1.5;

# Leemos el archivo con el mapa
df = pd.read_csv(input_file_map, sep='\s+', names=nombre_columnas, usecols=usa_columnas)
df = df.iloc[1:]

# definimos la función distancia entre dos puntos de una recta
def distancia_lineal(a,b):
    if (a > b):             
       return (a - b)
    else:
       return (b - a)

earlymeets = 0;   
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


# Calculamos la velocidad de conducción con un algoritmo muy simple
# Buscamos el punto más cercano y calculamos la velocidad con este y su LAT. 
'''
for index,row in df.iterrows():           
   dist = 10000;                          
   for index2,row2 in df.iterrows():     
       if index != index2:                
           ndist = ((row['x'] - row2['x'])**2 + (row['y'] - row2['y'])**2 + (row['z'] - row2['z'])**2)**(.5)
           if (ndist < dist):
               dist = ndist
               lastindex = index2          
   tiempo = distancia_lineal(df.loc[index, 'LAT'], df.loc[lastindex, 'LAT']);
   if (tiempo > 0):
       speed =  dist / distancia_lineal(df.loc[index, 'LAT'], df.loc[lastindex, 'LAT'])
   else:
       speed = fastest_speed;
   df.loc[index, 'Imp'] = speed;           

'''
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
            if ((distancia_lineal(row['x'], row2['x']) < radius) and (distancia_lineal(row['y'], row2['y']) < radius) and (distancia_lineal(row['z'], row2['z']) < radius)):
                lista_puntos.append(index2);
   speed = [];
   N = 0;
   for index2 in lista_puntos:
       distancia = (((df.loc[index, 'x']- df.loc[index2, 'x'])**2 + (df.loc[index, 'y']- df.loc[index2, 'y'])**2 + (df.loc[index, 'z']- df.loc[index2, 'z'])**2)**(.5));
       tiempo =  distancia_LAT(df.loc[index, 'LAT'],df.loc[index2, 'LAT'], CL);
       if (tiempo > 0 and distancia > minradius):
           nspeed = distancia / tiempo;
           speed.append(nspeed);
   if (len(speed) > minpoints):
       speed.remove(min(speed));
       df.loc[index, 'Imp'] = min(speed);
   else:
       df.loc[index, 'Imp'] = -1000;
       df.loc[index, 'del'] = -1;
      
   
# Quitamos los puntos donde no hemos podido medir    

# Algoritmo avanzado
  # Listar puntos cercanos, al menos 3
  # Calcular el plano que los incluye
  # Proyectar los puntos sobre el plano
  # Empezar con el vector de maximo incremento de LAT
  # Rotar el vector 15º Sobre el plano y calcular punto. 
  # Interporlar valor de LAT sobre ese punto, 
  # si es mayor volver a rotar 15º, si hemos pasado el máximo Asignar valor de velocidad. 
  # Rotar en la dirección contraria, y asignar el mayor de los dos. 
       
# Histograma de los valores,quitando los que no cumplen   
dfhist = df[df.Imp > 0]
print("Used points: " + str(100*len(dfhist)/len(df))+"%, " + str(len(dfhist)))
print("EarlyMeetsLate: " + str(100*len(dfhist)/earlymeets)+"%")
hist = dfhist.hist(column = 'Imp', bins=15)

# Exportamos a un archivo .sql
sql_sentence = "use Aces";
for index,row in df.iterrows():   
    sql_sentence = sql_sentence + "\nupdate points_table set impedance = " + str(df.loc[index,"Imp"]) +", deleted="+str(df.loc[index,"del"])+" where map_idx = " + str(map_idx) + " and sequential_index = "+ str(df.loc[index,"point_id"]);
sql_sentence = sql_sentence + "\ngo";
print(sql_sentence,  file = open(output_file, 'w'))

