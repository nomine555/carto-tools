@echo off
mode 240, 60
::
:: Mostramos la fecha
::
set datetime=%date%-%time%
set timestamp=%datetime:/=-%
set timestamp2=%timestamp::=-%
set timestamp3=%timestamp2:.=-%
set timestamp4=%timestamp3: =-%
::
echo System DateTime:  %datetime%
echo ----------------------------------------- 
echo Data Base DateTime
sqlcmd -i datetime.sql
::
:: Hacemos las consultas
::
sqlcmd -i viewtime.sql
sqlcmd -i listtime.sql > %timestamp4%-cartotimes.txt
pause
:: 
:: Cambia las comas por ;
:: 
:: ..\sed\sed.exe -i "s/,/;/g" *.csv
:: ..\sed\sed.exe -i "s/\./,/g" *.csv
:: del *.