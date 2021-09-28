#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 09:17:25 2019

@author: fernando
"""

import os
import datetime as dt
from struct import unpack
import numpy as np
import pandas as pd


# Variables de entrada
slash = "/";
input_file_map = "./tiempos.txt";
output_file = "./tiempos.csv";
rootdir = "./Fechas/Patients/";

dtime = dt.timedelta(hours = 0);

def filetime_to_dt(ft):
    EPOCH_AS_FILETIME = 116444736000000000  # January 1, 1970 as MS file time
    HUNDREDS_OF_NANOSECONDS = 10000000
    (s, ns100) = divmod(ft - EPOCH_AS_FILETIME, HUNDREDS_OF_NANOSECONDS)
    date = dt.datetime.fromtimestamp(s)
    date = date.replace(microsecond=(ns100 // 10))
    return date

# Load Database Data
tipos = {"STUDY_IDX":np.int}
df = pd.read_csv(input_file_map, sep='\s+', skiprows = {1}, skipfooter = 1, index_col=0, engine='python')
# df = df.drop(columns=['STUDY_IDX.1','STUDY_IDX.2']);

print("Procesando Estudios: ");
for paciente in os.listdir(rootdir):
    for estudio in os.listdir(rootdir + paciente + slash + "Studies"):    
        # Escogemos el archivo de log
        mtime = 2550132164.0;
        logfile = "";
        for file in os.listdir(rootdir + paciente + slash + "Studies" + slash + estudio + slash + "Log"):
            filename, file_extension = os.path.splitext(file)
            if file_extension == ".bin":
                ntime = os.path.getmtime(rootdir + paciente + slash + "Studies" + slash + estudio + slash + "Log" + slash + file);
                if (ntime < mtime):
                    mtime = ntime
                    logfile = file;
        # Número del estudio
        Nestudio = int(estudio[1:]);
        print(estudio);
        
        if (logfile != ""):
            # Buscamos el primer FAM
            with open(rootdir + paciente + slash + "Studies" + slash + estudio + slash +  "Log" + slash + logfile, "rb") as f:
                logbytes = f.read()
            N = logbytes.find(b"FAM_REQ_RECORDING_START")
            timestamp = unpack('<Q', logbytes[N-0x118:N-0x110]);       
            famstart = filetime_to_dt(timestamp[0]) + dtime;
        
            # Buscamos todas las veces el error 319.
            cathout = [];
            N = logbytes.find(b"Level: 'ERROR', ErrorMessage: '(319) MAP: catheter out of mapping range")
            while (N > 0):            
                timestamp = unpack('<Q',logbytes[N-0x113:N-0x10B]);       
                cathout.append(filetime_to_dt(timestamp[0]) + dtime);       
                N = logbytes.find(b"Level: 'ERROR', ErrorMessage: '(319) MAP: catheter out of mapping range",N + 1)
        
            # Si el estudio esta en BD
            if (Nestudio in df.index):
                df.loc[Nestudio, 'First_FAM'] = famstart.strftime('%H:%M:%S');
        
                # Escribimos la fecha de cateteres fuera
                lastRF = df.loc[Nestudio, 'Last_RF'];
                lastRF = dt.datetime.strptime("10/10/1900-" + lastRF[0:8], '%m/%d/%Y-%H:%M:%S')
                for date in cathout:
                    if (date.time() > lastRF.time()):
                        df.loc[Nestudio, 'Cath_Out'] = date.strftime('%H:%M:%S');
                        break;
                        
# Exportamos a csv.
df.to_csv(output_file);

        
        


        
        
