import os
import re
import subprocess

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 

input_file   = "..\\Visitag-Studies\\allrfs.csv";
dfn  = pd.read_csv(input_file, sep = ';', decimal=',', engine='python')


dfn = dfn[dfn['ImpedanceDrop'] != -10000]
dfn = dfn[dfn['ImpedanceDrop'] > 3]
dfn = dfn[dfn['ImpedanceDrop'] < 20]
dfn = dfn[dfn['MaxPower'] < 50]
dfn['fsd'] =  np.log(dfn['DurationTime'] * dfn['MaxTemperature']* dfn['MaxPower'] * dfn['MaxPower'] * dfn['MaxPower'] )
#dfn['fsd'] =  np.log(dfn['DurationTime'] * dfn['MaxPower'])
                  

linear_model  = np.polyfit(dfn['fsd'].to_numpy(),dfn['RFIndex'].to_numpy(),1)
funcion       = np.poly1d(linear_model)
x             = np.arange(dfn['fsd'].min(),dfn['fsd'].max())

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title("All points")
ax.scatter(dfn['RFIndex'].to_numpy(), dfn['fsd'].to_numpy())
ax.plot(funcion(x),x,color="green")
plt.show()



print(dfn['fsd'].corr(dfn['RFIndex']))


'''
print(dfn['BaseImpedance'].corr(dfn['RFIndex']))
print(dfn['DurationTime'].corr(dfn['RFIndex']))
print(dfn['MaxTemperature'].corr(dfn['RFIndex']))
print(dfn['MaxPower'].corr(dfn['RFIndex']))
'''
    