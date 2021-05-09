# awrExtractorAR
Extractor de valors per l'informe setmanal de Arquitectura Recurrent.

El extractor de valores es un bash script, se puede ejecutar desde linux o desde WSL en Windows 10.

## Requerimientos

- Python 3: **sudo apt-get install python3 python-is-python3**
- Pip (instalador de paquetes para python): **sudo apt-get install python3-pip**
- Librerías de python (dependencias de AWRp.py): **pip3 install pandas bs4 lxml tabulate**
- El fichero AWRp.py y dbvalues.sh deben estar en la misma carpeta

## Modo de empleo

**./dbvalues.sh <arw_fichero.html>**

El script acepta un solo parámetro que es el fichero AWR en formato HTML.

![alt text](https://github.com/agarciab/awrExtractorAR/blob/main/modo%20de%20empleo.PNG?raw=true)

## Salida

La salida del script contiene encabezados por la salida de error y los valores de las métricas por la salida estandar.
En cada linea hay un valor o bien está vacía para esa métrica en particular. Así se facilita el copy&paste en el excel de seguimiento.

El orden de salida de las métricas *Load Stats* (obtenidas de la tabla *Load Profile*):

1. DB Time/s
2. DB cpu/s
3. %Total CPU
4. Tx/s
5. Sql/tx

El orden de salida de las métricas *Foreground wait event* (en tanto por 1, obtenidas de la tabla *Top 10 Foreground Events by Total Wait Time*):

1. DB CPU
2. db file secuential read
3. direct path read
4. resmgr:cpu quantum
5. read by other session
6. db file parallel read
