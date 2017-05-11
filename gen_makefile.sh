#!/usr/bin/bash

declare -A deps_ej1
declare -A deps_ej2

while read line; do
	if [[ ! -z "$line" ]] && [[ ! $line =~ ^#+ ]]; then
		output="$(echo "${line}" | cut -f 1 -d ':')"
		cmd="$(echo "${line}" | cut -f 2 -d ':')"
		deps_ej1["tp1/ej1/pruebas/${output}"]="$cmd"
	fi
done < red_ej1.txt

while read line; do
	if [[ ! -z "$line" ]] && [[ ! $line =~ ^#+ ]]; then
		output="$(echo "${line}" | cut -f 1 -d ':')"
		cmd="$(echo "${line}" | cut -f 2 -d ':')"
		deps_ej2["tp1/ej2/pruebas/${output}"]="$cmd"
	fi
done < red_ej2.txt

cat <<EOT
PYTHON=python3
SCRIPT_TABLA_EJ1=tp1/ej1/build_table.sh
TABLA_EJ1=tp1/ej1/pruebas/aciertos.txt

DATA_EJ1=\\
EOT
for key in ${!deps_ej1[@]}; do
    echo "${key} \\"
done

cat <<EOT

DATA_EJ2=\\
EOT
for key in ${!deps_ej2[@]}; do
    echo "${key} \\"
done

cat <<EOT

ERRORES_EJ1=\$(subst .dat,_errors.png,\${DATA_EJ1})

ERRORES_EJ2=\$(subst .dat,_errors.png,\${DATA_EJ2})

all: \${ERRORES_EJ1} \${ERRORES_EJ2} \${DATA_EJ1} \${DATA_EJ2} \${TABLA_EJ1}


%_errors.png: %.dat
	gnuplot -e "datafile='$<'" tp1/plot/errores.gpi > \$@
EOT

for key in ${!deps_ej1[@]}; do
    echo "${key}:"
    echo -e "\t\${PYTHON} ./ej1-runner.py ${deps_ej1[$key]} > \$@"
done

for key in ${!deps_ej2[@]}; do
    echo "${key}:"
    echo -e "\t\${PYTHON} ./ej2-runner.py ${deps_ej2[$key]} > \$@"
done

cat <<EOT
\${TABLA_EJ1}: \${DATA_EJ1}
	\${SCRIPT_TABLA_EJ1} \$^ > \$@
clean:
	rm -rf \${ERRORES_EJ1} \${ERRORES_EJ2} \${DATA_EJ1} \${DATA_EJ2} \${TABLA_EJ1}
.PHONY: clean
EOT
