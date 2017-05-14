import sys
import argparse
from tp1 import rn
from tp1 import af
from tp1 import lm
from tp1.utils import random_uniform

ETA=0.03
EPOCHS=100

def parse_argv(ej):
    TRAINING_DB = (r'tp1/ej1/data/tp1_ej1_training.csv', r'tp1/ej2/data/tp1_ej2_training.csv')
    parser = argparse.ArgumentParser(description='Entrena/Testea una red neuronal')
    parser.add_argument('--db', type=str, help="Base de datos", default=TRAINING_DB[ej])
    parser.add_argument('--train', dest='train', action='store_true', help="Modo entrenamiento")
    parser.add_argument('--test', dest='train', action='store_false', help="Modo test")
    parser.add_argument('units', type=str, help="Cantidad de entradas por capa. Ejemplo: '10-20-1'")
    parser.add_argument('act_units', type=str, help="Activacion unidades de salida. Ejemplo: 'l-t-s'")
    training_mode_choices = ('stochastic', 'online', 'batch', 'mini_batch')
    parser.add_argument('-t', '--training-mode', choices=training_mode_choices, default='stochastic', help="Modo de entrenamiento")
    parser.add_argument('-n', '--eta', type=float, default=ETA)
    parser.add_argument('-e', '--epochs', type=int, default=EPOCHS)
    parser.add_argument('--alpha', type=float)
    parser.add_argument('-a', '--a', type=float)
    parser.add_argument('-b', '--b', type=float)
    parser.add_argument('--batch_size', type=int)
    parser.add_argument('--training-prop', type=float, default=0.6)
    parser.add_argument('--normalize-input', dest='normalize_input', action='store_true')
    parser.add_argument('--no-normalize-input', dest='normalize_input', action='store_false')
    parser.add_argument('--normalize-output', dest='normalize_output', action='store_true')
    parser.add_argument('--no_normalize-output', dest='normalize_output', action='store_false')
    parser.add_argument('--random-funct', choices=('normal', 'uniform'))
    parser.set_defaults(normalize_input=True, normalize_output=False, train=True)
    args = parser.parse_args()



    def salir(msg):
        print(msg)
        sys.exit(1)

    if not args.train:
        return {'train': False,
                'db' : args.db}

    if args.training_prop > 1.0:
        salir("Se esperaba una proporcion de training entre 0 y 1")


    activation_choices = ('sign', 's', 'sigmoid', 'l', 't', 'tanh', 'r', 'ReLu', 'i', 'identity')

    def parse_act_str(act_str):
        if act_str in ('sign', 's'):
            return af.sign()
        elif act_str in ('tanh', 't'):
            return af.tanh()
        elif act_str in ('t2'):
            return af.tanh(0.125)
        elif act_str in ('sigmoid', 'l'):
            return af.sigmoid()
        elif act_str in ('ReLu', 'r'):
            return af.ReLu()
        elif act_str in ('i', 'id', 'identity'):
            return af.identity()
        else:
            salir("{}: Funcion de activacion desconocida. Opciones={}".format(act_str, ",".join(activation_choices)))


    ns = list(map(int, args.units.split("-")))
    gs = list(map(parse_act_str, args.act_units.split("-")))

    if len(gs) != len(ns)-1:
        salir("Se esperaba la misma cantidad de funciones de activacion que de capas")

    if args.random_funct:
        if args.random_funct == 'normal':
            random_funct = RN.random_funct
        else:
            random_funct = random_uniform

    if args.random_funct:
        red = rn.RN(ns=ns, gs=gs, random_funct=random_funct)
    else:
        red = rn.RN(ns=ns, gs=gs)

    if args.training_mode in ('stochastic', 'online'):
        training_mode = lm.TrainMode.STOCHASTIC
    elif args.training_mode in ('batch'):
        training_mode = lm.TrainMode.BATCH
    else:
        training_mode = lm.TrainMode.MINI_BATCH

    learn_params = dict({'training_mode' : training_mode,
                         'eta' : args.eta,
                         'epochs' : args.epochs})
    if training_mode == lm.TrainMode.MINI_BATCH:
        if args.batch_size:
            learn_params['batch_size'] = args.batch_size
        else:
            learn_params['batch_size'] = 10

    if args.a:
        learn_params['a'] = args.a
    if args.b:
        learn_params['b'] = args.b
    if args.alpha:
        learn_params['alpha'] = args.alpha

    if args.alpha or args.a or args.b:
        tutor = lm.BackPropagationOptimized(red)
    else:
        tutor = lm.BackPropagation(red)

    if args.a or args.b:
        learn_funct = tutor.learn_adaptative
    else:
        learn_funct = tutor.learn

    return {'train' : True,
            'db' : args.db,
            'learn_funct': learn_funct,
            'learn_params' : learn_params,
            'normalize_input' : args.normalize_input,
            'normalize_output' : args.normalize_output,
            'training_prop' : args.training_prop,
            'red' : red}
