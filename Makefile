PYTHON=python3
SCRIPT_TABLA=tp1/ej1/pruebas/build_table.sh
TABLA=tp1/ej1/pruebas/aciertos.txt

DATA=tp1/ej1/pruebas/ex_1-1_red_11-1.dat \
     tp1/ej1/pruebas/ex_1_1_red_11-21-1.dat \
     tp1/ej1/pruebas/ex_1_1_red_11-6-6-9-1.dat \
     tp1/ej1/pruebas/ex_2_1_red_11-21-1.dat \
     tp1/ej1/pruebas/ex_2_2_red_11-21-1.dat \
     tp1/ej1/pruebas/ex_2_3_red_11-21-1.dat \
     tp1/ej1/pruebas/ex_2_4_red_11-21-1.dat \
     tp1/ej1/pruebas/ex_2_1_red_11-6-6-9-1.dat \
     tp1/ej1/pruebas/ex_2_2_red_11-6-6-9-1.dat \
     tp1/ej1/pruebas/ex_2_3_red_11-6-6-9-1.dat \
     tp1/ej1/pruebas/ex_2_4_red_11-6-6-9-1.dat
DATA=tp1/ej1/pruebas/ex_1-1_red_11-1_errors.png \
     tp1/ej1/pruebas/ex_1_1_red_11-21-1_errors.png \
     tp1/ej1/pruebas/ex_1_1_red_11-6-6-9-1_errors.png \
     tp1/ej1/pruebas/ex_2_1_red_11-21-1_errors.png \
     tp1/ej1/pruebas/ex_2_2_red_11-21-1_errors.png \
     tp1/ej1/pruebas/ex_2_3_red_11-21-1_errors.png \
     tp1/ej1/pruebas/ex_2_4_red_11-21-1_errors.png \
     tp1/ej1/pruebas/ex_2_1_red_11-6-6-9-1_errors.png \
     tp1/ej1/pruebas/ex_2_2_red_11-6-6-9-1_errors.png \
     tp1/ej1/pruebas/ex_2_3_red_11-6-6-9-1_errors.png \
     tp1/ej1/pruebas/ex_2_4_red_11-6-6-9-1_errors.png
# ACIERTOS=tp1/ej1/pruebas/ex_1_plot_11-1_eta_0.03_aciertos.png \
#          tp1/ej1/pruebas/ex_1_plot_11-6-1_eta_0.03_aciertos.png \
#          tp1/ej1/pruebas/ex_1_plot_11-21-1_eta_0.03_aciertos.png \
#          tp1/ej1/pruebas/ex_1_plot_11-6-6-9-1_eta_0.03_aciertos.png \
#          tp1/ej1/pruebas/ex_1_plot_11-16-21-6-1_eta_0.03_aciertos.png \
#          tp1/ej1/pruebas/ex_1_plot_11-11-11-11-11-1_eta_0.03_aciertos.png

all: ${ERRORES} ${DATA} ${TABLA}

%_errors.png: %.dat
	gnuplot -e "datafile='$<'" tp1/ej1/errores.gpi > $@

tp1/ej1/pruebas/ex_1-1_%.dat:
	${PYTHON} ej1-runner.py 0 0

tp1/ej1/pruebas/ex_2-1_%.dat:
	${PYTHON} ej1-runner.py 1 0

tp1/ej1/pruebas/ex_2-2_%.dat:
	${PYTHON} ej1-runner.py 1 1

tp1/ej1/pruebas/ex_2-3_%.dat:
	${PYTHON} ej1-runner.py 1 2

tp1/ej1/pruebas/ex_2-4_%.dat:
	${PYTHON} ej1-runner.py 1 3

${TABLA}: ${DATA}
	${SCRIPT_TABLA} $< > $@

clean:
	rm -rf ${ERRORES} ${ACIERTOS} ${DATA}

.PHONY: clean
