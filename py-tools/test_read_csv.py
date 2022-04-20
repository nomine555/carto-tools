# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 16:46:08 2022

@author: Nomine
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 


#input_file = "..\..\Estudios\Estudios-powerfast\\1242184-FA\Sites.txt"
#input_file2 = "..\..\Estudios\Estudios-powerfast\\1242184-FA\VisiTagSessions.txt"

input_file = "..\..\Estudios\Estudios-powerfast\\0275411-FA_Powerfast70\Sites.txt"
input_file2 = "..\..\Estudios\Estudios-powerfast\\0275411-FA_Powerfast70\VisiTagSessions.txt"


#df  = pd.read_csv(input_file, sep='\s+', index_col=0, engine='python')
#df2 = pd.read_csv(input_file2, sep='\s+', index_col=0, engine='python')
df  = pd.read_fwf(input_file, index_col=0, widths=[20,20,20,20,20,20,20,20,20,20,20,20,20,20,20], engine='python')
df2 = pd.read_fwf(input_file2, index_col=0,widths=[20,20,20,20,20,20], engine='python')
        
dfn = df.join(df2)
dfn.reset_index(level=0, inplace=True)

        