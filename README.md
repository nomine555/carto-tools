
# INTRODUCTION
I have developed this tools to help me in obtaining data from Carto Electrophysiology Navigator by Biosense Webster. 
Also I have done some research on propagation velocity and inter-lesion distance of lesions. 
Here you have all the different directories:

* Assets
 * This are exported files from Carto for playing and testing. 

* AutoHotkey-tools
    * This are on screen scripts to help me with repetitive tasks. 
    * Cartobakup.ahk
        * This script clicks on “ok” every time a DICOM file is imported with errors. 
    * Visigat.ahk
        * This script exports all the data of a Carto System in order to have it for research, without the need to enter on every case. 

* Py-tools
    * Carto.py
        * Algorithm for conduction velocity on a Carto map. 
    * Regression.py
        * Estimate Tag Index value based on Power, Impedance and Temperature. (it works quite well, it’s like AI without Force)
    * Tiempos.py
        * Looking on Carto Log Files in order to get the “time” you clicked on FAM button for the first time. This is used to get times from Carto automatically. 
    * Velocidad.py
        * Algorithm for conduction velocity on a Carto map.
    * Visitag_directorio.py
        * This tools calculates inter-lesion distance. 
    * Visitag.ini
        * The configuration of the previous script

* Sql-tools
    * Lista-tiempos.bat
        * Uses all the “sql” scripts, list and sends to file, all the times and cases. 
        * Once the Carto is started, first point acquired, First ablation started and last ablation. 
        
*	Visitag-tools
    * This is the compiled version of visitag_directorio.py, in order to any one use it without knowledge. 

## Visitag-tools

It has three parts:

1.	First we load data from Carto System directly avoiding the need to export data manually. 
2.	Then we segment in lesions groups semi-automatically.
3.	Finally, we use the Floyd-Warshall algorithm with a special distance function, in order to get the sequences of visitags that encircle a vein. 

## Contacting me

You can find me on linkedin, my name is Fernando Setien Dodero.  

## Related projects

This guys are working on something much bigger https://github.com/openep/
