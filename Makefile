PYTHON=python3
SCRIPT_TABLA_EJ1=tp1/ej1/build_table.sh
TABLA_EJ1=tp1/ej1/pruebas/aciertos.txt

DATA_EJ1=tp1/ej1/pruebas/ex_1-1_red_11-1.dat \
         tp1/ej1/pruebas/ex_1-1_red_11-21-1.dat \
         tp1/ej1/pruebas/ex_1-1_red_11-6-6-9-1.dat \
         tp1/ej1/pruebas/ex_2-1_red_11-21-1.dat \
         tp1/ej1/pruebas/ex_2-2_red_11-21-1.dat \
         tp1/ej1/pruebas/ex_2-3_red_11-21-1.dat \
         tp1/ej1/pruebas/ex_2-4_red_11-21-1.dat \
         tp1/ej1/pruebas/ex_2-1_red_11-6-6-9-1.dat \
         tp1/ej1/pruebas/ex_2-2_red_11-6-6-9-1.dat \
         tp1/ej1/pruebas/ex_2-3_red_11-6-6-9-1.dat \
         tp1/ej1/pruebas/ex_2-4_red_11-6-6-9-1.dat \
         tp1/ej1/pruebas/ex_3-1_red_11-6-6-9-1.dat \
         tp1/ej1/pruebas/ex_3-2_red_11-6-6-9-1.dat \
         tp1/ej1/pruebas/ex_4-1_red_11-6-6-9-1.dat \
         tp1/ej1/pruebas/ex_4-2_red_11-6-6-9-1.dat \
         tp1/ej1/pruebas/ex_4-3_red_11-6-6-9-1.dat \

DATA_EJ2=tp1/ej2/pruebas/ex_1-1_red_9-17-7-2.dat \
         tp1/ej2/pruebas/ex_1-1_red_9-7-17-2.dat

ERRORES_EJ1=$(subst .dat,_errors.png,${DATA_EJ1})

ERRORES_EJ2=$(subst .dat,_errors.png,${DATA_EJ2})

all: ${ERRORES_EJ1} ${ERRORES_EJ2} ${DATA_EJ1} ${DATA_EJ2} ${TABLA_EJ1}


%_errors.png: %.dat
	gnuplot -e "datafile='$<'" tp1/plot/errores.gpi > $@

tp1/ej1/pruebas/ex_1-1_%.dat:
	${PYTHON} ej1-runner.py 0 0

tp1/ej2/pruebas/ex_1-1_%.dat:
	${PYTHON} ej2-runner.py 0 0

tp1/ej1/pruebas/ex_2-1_%.dat:
	${PYTHON} ej1-runner.py 1 0

tp1/ej1/pruebas/ex_2-2_%.dat:
	${PYTHON} ej1-runner.py 1 1

tp1/ej1/pruebas/ex_2-3_%.dat:
	${PYTHON} ej1-runner.py 1 2

tp1/ej1/pruebas/ex_2-4_%.dat:
	${PYTHON} ej1-runner.py 1 3

tp1/ej1/pruebas/ex_3-1_%.dat:
	${PYTHON} ej1-runner.py 2 0

tp1/ej1/pruebas/ex_3-2_%.dat:
	${PYTHON} ej1-runner.py 2 1

tp1/ej1/pruebas/ex_4-1_%.dat:
	${PYTHON} ej1-runner.py 3 0

tp1/ej1/pruebas/ex_4-2_%.dat:
	${PYTHON} ej1-runner.py 3 1

tp1/ej1/pruebas/ex_4-3_%.dat:
	${PYTHON} ej1-runner.py 3 2

${TABLA_EJ1}: ${DATA_EJ1}
	${SCRIPT_TABLA_EJ1} $^ > $@

clean:
	rm -rf ${ERRORES_EJ1} ${ERRORES_EJ2} ${DATA_EJ1} ${DATA_EJ2} ${TABLA_EJ1}

.PHONY: clean
