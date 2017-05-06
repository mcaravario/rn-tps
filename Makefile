PYTHON=python3

DATA=tp1/ej1/pruebas/ex_1_plot_11-1_eta_0.03.dat \
     tp1/ej1/pruebas/ex_1_plot_11-21-1_eta_0.03.dat \
     tp1/ej1/pruebas/ex_1_plot_11-6-6-9-1_eta_0.03.dat \
     tp1/ej1/pruebas/ex_2_plot_11-21-1_eta_0.3_alpha_0.01.dat \
     tp1/ej1/pruebas/ex_2_plot_11-21-1_eta_0.05_alpha_0.01.dat \
     tp1/ej1/pruebas/ex_2_plot_11-21-1_eta_0.05_alpha_0.3.dat \
     tp1/ej1/pruebas/ex_2_plot_11-21-1_eta_0.3_alpha_0.3.dat \
     tp1/ej1/pruebas/ex_2_plot_11-6-6-9-1_eta_0.3_alpha_0.01.dat \
     tp1/ej1/pruebas/ex_2_plot_11-6-6-9-1_eta_0.05_alpha_0.01.dat \
     tp1/ej1/pruebas/ex_2_plot_11-6-6-9-1_eta_0.05_alpha_0.3.dat \
     tp1/ej1/pruebas/ex_2_plot_11-6-6-9-1_eta_0.3_alpha_0.3.dat
ERRORES=tp1/ej1/pruebas/ex_1_plot_11-1_eta_0.03_errors.png \
        tp1/ej1/pruebas/ex_1_plot_11-21-1_eta_0.03_errors.png \
        tp1/ej1/pruebas/ex_1_plot_11-6-6-9-1_eta_0.03_errors.png \
        tp1/ej1/pruebas/ex_2_plot_11-21-1_eta_0.3_alpha_0.01_errors.png \
        tp1/ej1/pruebas/ex_2_plot_11-21-1_eta_0.05_alpha_0.01_errors.png \
        tp1/ej1/pruebas/ex_2_plot_11-21-1_eta_0.05_alpha_0.3_errors.png \
        tp1/ej1/pruebas/ex_2_plot_11-21-1_eta_0.3_alpha_0.3_errors.png \
        tp1/ej1/pruebas/ex_2_plot_11-6-6-9-1_eta_0.3_alpha_0.01_errors.png \
        tp1/ej1/pruebas/ex_2_plot_11-6-6-9-1_eta_0.05_alpha_0.01_errors.png \
        tp1/ej1/pruebas/ex_2_plot_11-6-6-9-1_eta_0.05_alpha_0.3_errors.png \
        tp1/ej1/pruebas/ex_2_plot_11-6-6-9-1_eta_0.3_alpha_0.3_errors.png
# ACIERTOS=tp1/ej1/pruebas/ex_1_plot_11-1_eta_0.03_aciertos.png \
#          tp1/ej1/pruebas/ex_1_plot_11-6-1_eta_0.03_aciertos.png \
#          tp1/ej1/pruebas/ex_1_plot_11-21-1_eta_0.03_aciertos.png \
#          tp1/ej1/pruebas/ex_1_plot_11-6-6-9-1_eta_0.03_aciertos.png \
#          tp1/ej1/pruebas/ex_1_plot_11-16-21-6-1_eta_0.03_aciertos.png \
#          tp1/ej1/pruebas/ex_1_plot_11-11-11-11-11-1_eta_0.03_aciertos.png

all: ${ERRORES} ${DATA}

%_errors.png: %.dat
	gnuplot -e "datafile='$<'" tp1/ej1/errores.gpi > $@

ex_1_%.dat:
	${PYTHON} ej1-runner.py 0

ex_2_%.dat:
	${PYTHON} ej1-runner.py 1

clean:
	rm -rf ${ERRORES} ${ACIERTOS} ${DATA}

.PHONY: clean
