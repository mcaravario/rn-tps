#!/bin/bash
echo "\\begin{matrix}[c|c|c|c|c]"
echo -e "\tArchivo & Mejor % de aciertos training & Mejor % de validacion & Mejor % de validacion \\\\"
for filename in $@; do
	max_training=`cat "$filename" | sort -n -k4r | head -n 1 | awk '{print $4,"("$1,"epochs)"}'`
	max_validation=`cat "$filename" | sort -n -k7 | sort -n --stable -k5r | head -n 1 | awk '{print $5,"("$1,"epochs) & ",$6,"&",$7;}'`
	echo -e "\t$filename & ${max_training} & ${max_validation} \\\\"
done
echo "\\end{matrix}"
