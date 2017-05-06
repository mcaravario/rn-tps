PYTHON=python3

DATA=tp1/ej1/pruebas/ex_1_plot_11-1_ep_500_eta_0.03.dat \
     tp1/ej1/pruebas/ex_1_plot_11-6-1_ep_500_eta_0.03.dat \
     tp1/ej1/pruebas/ex_1_plot_11-21-1_ep_500_eta_0.03.dat \
     tp1/ej1/pruebas/ex_1_plot_11-6-6-9-1_ep_500_eta_0.03.dat \
     tp1/ej1/pruebas/ex_1_plot_11-16-21-6-1_ep_500_eta_0.03.dat \
     tp1/ej1/pruebas/ex_1_plot_11-11-11-11-11-1_ep_500_eta_0.03.dat
ERRORES=tp1/ej1/pruebas/ex_1_plot_11-1_ep_500_eta_0.03_errors.png \
        tp1/ej1/pruebas/ex_1_plot_11-6-1_ep_500_eta_0.03_errors.png \
        tp1/ej1/pruebas/ex_1_plot_11-21-1_ep_500_eta_0.03_errors.png \
        tp1/ej1/pruebas/ex_1_plot_11-6-6-9-1_ep_500_eta_0.03_errors.png \
        tp1/ej1/pruebas/ex_1_plot_11-16-21-6-1_ep_500_eta_0.03_errors.png \
        tp1/ej1/pruebas/ex_1_plot_11-11-11-11-11-1_ep_500_eta_0.03_errors.png
ACIERTOS=tp1/ej1/pruebas/ex_1_plot_11-1_ep_500_eta_0.03_aciertos.png \
         tp1/ej1/pruebas/ex_1_plot_11-6-1_ep_500_eta_0.03_aciertos.png \
         tp1/ej1/pruebas/ex_1_plot_11-21-1_ep_500_eta_0.03_aciertos.png \
         tp1/ej1/pruebas/ex_1_plot_11-6-6-9-1_ep_500_eta_0.03_aciertos.png \
         tp1/ej1/pruebas/ex_1_plot_11-16-21-6-1_ep_500_eta_0.03_aciertos.png \
         tp1/ej1/pruebas/ex_1_plot_11-11-11-11-11-1_ep_500_eta_0.03_aciertos.png

all: ${ERRORES} ${ACIERTOS} ${DATA}

%_errors.png: %.dat
	gnuplot -e "datafile='$<'" tp1/ej1/errores.gpi > $@

%_aciertos.png: %.dat
	gnuplot -e "datafile='$<'" tp1/ej1/aciertos.gpi > $@

ex_1_%.dat:
	${PYTHON} ej1-runner.py 0

clean:
	rm -rf ${ERRORES} ${ACIERTOS} ${DATA}

.PHONY: clean
