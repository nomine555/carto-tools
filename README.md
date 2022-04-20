
# INTRODUCTION
I have developed this tools to help me in obtaining data from Carto Electrophysiology Navigator by Biosense Webster. 
Also I have done some research on propagation velocity and inter-lesion distance of lesions. 
Here you have all the different directories:


* AutoHotkey-tools
    * This are on screen scripts that help me with repetitive tasks. 
    * Cartobakup.ahk
        * This script clicks on “ok” every time a DICOM file is imported with errors. 
    * Visigat.ahk
        * This script exports all the data of a Carto System in order to have it for research, without the need to enter on every case. 

* Py-tools
    * Carto.py & Velocidad.py        
        * Algorithm for calculation conduction velocity on a Carto map. 
    * Regression.py
        * Estimate Tag Index value based on Power, Impedance and Temperature. (it works quite well R = 0.8, it’s like BW TagIndex but without using Force value)
    * Tiempos.py
        * Looking on Carto Log Files in order to get the “time” you clicked on FAM button for the first time. This is used to get times of a Carto case automatically. 
    * Visitag_directorio.py
        * This tools calculates inter-lesion distance. 
    * Visitag.ini
        * The configuration of the previous script

* Sql-tools
    * Lista-tiempos.bat
        * Uses all the “sql” scripts, list and sends to file, all the times and cases. 
        * Ex: Once the Carto is started, first point acquired, First ablation started, last ablation, last point adquired and las map edited. 
        
*	Visitag-tools
    * This is the compiled version of visitag_directorio.py, easy to use. 

* Assets
    * Carto exported files for testing. 


## Visitag-tools

It does the following:

1.	Load data from Carto System directly avoiding the need to export data manually. 
2.	Segment lesions in groups semi-automatically. It's just ask for confirmation or try with a different number of segments. 
3.	Using Floyd-Warshall algorithm with a special distance function, we get the sequences of visitags that encircle a vein. 
4.  It shows a plot, so you can check manually if the algorithm has worked correctly.  
5.  Finally we calculate mean, standar deviation and 95% confidence interval of lesions distances and export all to a .csv file. 

## Contacting me

You can find me on linkedin, my name is Fernando Setien Dodero.  

## Related projects

This guys are serius working on something much bigger https://github.com/openep/
