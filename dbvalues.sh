#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: ./dbvalues.sh <awr_file_name.html>"
	exit 1
fi

>&2 echo "--- LOAD STATS (DB time, DB cpu, Total %CPU, TX/s, SQL/tx ---"
python AWRp.py -fmt csv -sections 2 -files $1 2> /dev/null | head -3 | tail -2 | cut -f2 -d, #### DB Time & DB CPU
python AWRp.py -fmt csv -sections 3 -files $1 2> /dev/null | tail -2 | head -1 | cut -f1 -d, #### Total % CPU
python AWRp.py -fmt csv -sections 2 -files $1 2> /dev/null | tail -2 | head -1 | cut -f2 -d, #### TX/S
python AWRp.py -fmt csv -sections 2 -files $1 2> /dev/null | tail -4 | head -1 | cut -f3 -d, #### SQL/TX
>&2 echo "--- WAIT EVENTS (en tanto por uno)---"

### WAITs ###
metric=("DB CPU" "db file sequential read" "direct path read" "resmgr:cpu quantum" "read by other session" "db file parallel read")
for i in "${metric[@]}"
do
    val=$(python AWRp.py -fmt csv -sections 4 -files $1 2> /dev/null | grep "$i" | sed -Ee :1 -e 's/^(([^",]|"[^"]*")*),/\1;/;t1' | cut -f5 -d';')
	if [ -z "$val" ];
	then
		echo ""
	else
		echo "scale=3; $val / 100" | bc -l
	fi
done




