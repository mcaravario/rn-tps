PYTHON=python3
SCRIPT_TABLA_EJ1=tp1/ej1/build_table.sh
TABLA_EJ1=tp1/ej1/pruebas/aciertos.txt

DATA_EJ1=\
tp1/ej1/pruebas/ex_4-3_red_11-6-6-9-1.dat \
tp1/ej1/pruebas/ex_2-4_red_11-6-6-9-1.dat \
tp1/ej1/pruebas/ex_1-2_red_11-1.dat \
tp1/ej1/pruebas/ex_2-4_red_11-21-1.dat \
tp1/ej1/pruebas/ex_2-2_red_11-6-6-9-1.dat \
tp1/ej1/pruebas/ex_1-3_red_11-1.dat \
tp1/ej1/pruebas/ex_2-3_red_11-21-1.dat \
tp1/ej1/pruebas/ex_4-2_red_11-6-6-9-1.dat \
tp1/ej1/pruebas/ex_2-1_red_11-21-1.dat \
tp1/ej1/pruebas/ex_1-1_red_11-1.dat \
tp1/ej1/pruebas/ex_2-3_red_11-6-6-9-1.dat \
tp1/ej1/pruebas/ex_2-1_red_11-6-6-9-1.dat \
tp1/ej1/pruebas/ex_4-1_red_11-6-6-9-1.dat \
tp1/ej1/pruebas/ex_3-1_red_11-6-6-9-1.dat \
tp1/ej1/pruebas/ex_2-2_red_11-21-1.dat \
tp1/ej1/pruebas/ex_3-2_red_11-6-6-9-1.dat \

ERRORES_EJ1=$(subst .dat,_errors.png,${DATA_EJ1})

ERRORES_EJ2=$(subst .dat,_errors.png,${DATA_EJ2})

all: ${ERRORES_EJ1} ${ERRORES_EJ2} ${DATA_EJ1} ${DATA_EJ2} ${TABLA_EJ1}


%_errors.png: %.dat
	gnuplot -e "datafile='$<'" tp1/plot/errores.gpi > 
tp1/ej1/pruebas/ex_4-3_red_11-6-6-9-1.dat:
	./ej1-runner.py  10-5-5-8-1 l-l-l-s --eta=0.03 --alpha=0.1 --training-mode='mini_batch' --batch_size=50 --epochs=1000 > $@
tp1/ej1/pruebas/ex_2-4_red_11-6-6-9-1.dat:
	./ej1-runner.py  10-5-5-8-1 l-l-l-s --eta=0.07 --alpha=0.3 --training-mode='stochastic' --epochs=1000 > $@
tp1/ej1/pruebas/ex_1-2_red_11-1.dat:
	./ej1-runner.py  10-20-1 l-s        --eta=0.03 --training-mode='stochastic' --epochs=1000 > $@
tp1/ej1/pruebas/ex_2-4_red_11-21-1.dat:
	./ej1-runner.py  10-20-1 l-s --eta=0.07 --alpha=0.3 --training-mode='stochastic' --epochs=1000 > $@
tp1/ej1/pruebas/ex_2-2_red_11-6-6-9-1.dat:
	./ej1-runner.py  10-5-5-8-1 l-l-l-s --eta=0.03 --alpha=0.1 --training-mode='stochastic' --epochs=1000 > $@
tp1/ej1/pruebas/ex_1-3_red_11-1.dat:
	./ej1-runner.py  10-5-5-8-1 l-l-l-s --eta=0.03 --training-mode='stochastic' --epochs=1000 > $@
tp1/ej1/pruebas/ex_2-3_red_11-21-1.dat:
	./ej1-runner.py  10-20-1 l-s --eta=0.03 --alpha=0.3 --training-mode='stochastic' --epochs=1000 > $@
tp1/ej1/pruebas/ex_4-2_red_11-6-6-9-1.dat:
	./ej1-runner.py  10-5-5-8-1 l-l-l-s --eta=0.03 --alpha=0.1 --training-mode='mini_batch' --batch_size=50 --epochs=1000 > $@
tp1/ej1/pruebas/ex_2-1_red_11-21-1.dat:
	./ej1-runner.py  10-20-1 l-s --eta=0.07 --alpha=0.1 --training-mode='stochastic' --epochs=1000 > $@
tp1/ej1/pruebas/ex_1-1_red_11-1.dat:
	./ej1-runner.py  10-1 s             --eta=0.03 --training-mode='stochastic' --epochs=1000 > $@
tp1/ej1/pruebas/ex_2-3_red_11-6-6-9-1.dat:
	./ej1-runner.py  10-5-5-8-1 l-l-l-s --eta=0.03 --alpha=0.3 --training-mode='stochastic' --epochs=1000 > $@
tp1/ej1/pruebas/ex_2-1_red_11-6-6-9-1.dat:
	./ej1-runner.py  10-5-5-8-1 l-l-l-s --eta=0.07 --alpha=0.1 --training-mode='stochastic' --epochs=1000 > $@
tp1/ej1/pruebas/ex_4-1_red_11-6-6-9-1.dat:
	./ej1-runner.py  10-5-5-8-1 l-l-l-s --eta=0.03 --alpha=0.1 --training-mode='batch' --epochs=1000 > $@
tp1/ej1/pruebas/ex_3-1_red_11-6-6-9-1.dat:
	./ej1-runner.py  10-5-5-8-1 l-l-l-s --eta=0.03 --alpha=0.1 --a=0.02 --b=0.7 --training-mode='stochastic' --epochs=1000 > $@
tp1/ej1/pruebas/ex_2-2_red_11-21-1.dat:
	./ej1-runner.py  10-20-1 l-s --eta=0.03 --alpha=0.1 --training-mode='stochastic' --epochs=1000 > $@
tp1/ej1/pruebas/ex_3-2_red_11-6-6-9-1.dat:
	./ej1-runner.py  10-5-5-8-1 l-l-l-s --eta=0.03 --alpha=0.1 --a=0.02 --b=0.1 --training-mode='stochastic' --epochs=1000 > $@
${TABLA_EJ1}: ${DATA_EJ1}
	${SCRIPT_TABLA_EJ1} $^ > $@
clean:
	rm -rf ${ERRORES_EJ1} ${ERRORES_EJ2} ${DATA_EJ1} ${DATA_EJ2} ${TABLA_EJ1}
.PHONY: clean
