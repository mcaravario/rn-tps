import argparse
import rn
import af
import lm

ETA=0.03
EPOCHS=100

def load_training_validation(training_db, training_prop=0.6):
    TRAINING_DB = r'tp1/ej2/data/tp1_ej2_training.csv'
    df = pd.read_csv(training_db, header=None)

    outputs = df[df.columns[-2:]].as_matrix()
    inputs = df[df.columns[:-2]].as_matrix()

    data = list(zip(inputs, outputs))

    training_size = int(training_prop * len(data))

    choices = [True for i in range(training_size)] + [False for j in range(len(data)-training_size)]
    random.shuffle(choices)

    training = list(compress(data, choices))
    validation = list(compress(data, map(lambda x: 1-x, choices)))

    return training, validation

def parse_argv():
    TRAINING_DB = (r'tp1/ej1/data/tp1_ej1_training.csv', r'tp1/ej2/data/tp1_ej2_training.csv')
    parser = argparse.ArgumentParser(description='Entrena una red neuronal')
    parser.add_argument('--ej', choices=(1, 2), default=1, type=int)
    parser.add_argument('input_units', metavar='U', type=int, nargs=1, help="Cantidad de entradas")
    parser.add_argument('hidden_units', metavar='U', type=int, nargs='*', help="Cantidad de unidades ocultas")
    parser.add_argument('output_units', metavar='U', type=int, nargs=1, help="Cantidad de salidas")
    activation_choices = ('sign', 's', 'sigmoid', 'l', 't', 'tanh', 'r', 'ReLu', 'i', 'identity')
    parser.add_argument('act_hidden_units', metavar='g', choices=activation_choices, type=int, nargs='*', help="Activacion unidades ocultas")
    parser.add_argument('act_output_units', metavar='g', choices=activation_choices, type=int, nargs=1, help="Activacion unidades de salida")
    training_mode_choices = ('stochastic', 'online', 'batch', 'mini_batch')
    parser.add_argument('-t', '--training-mode', choices=training_mode_choices, default='stochastic', help="Modo de entrenamiento")
    parser.add_argument('-n', '--eta', type=float, default=ETA)
    parser.add_argument('-e', '--epochs', type=int, default=EPOCHS)
    parser.add_argument('--alpha', type=float)
    parser.add_argument('-a', '--a', type=float)
    parser.add_argument('-b', '--b', type=float)
    parser.add_argument('--batch_size', type=int)
    args = parser.parse_args()

    def salir(msg):
        print(msg)
        sys.exit(1)

    if len(args.hidden_units) != len(args.act_hidden_units):
        salir("Se esperaba la misma cantidad de funciones de activacion que de capas")

    if args.ej == 1:
        if len(args.input_units) != 10:
            salir("Numero erroneo de entradas: {}".format(args.input_units))
        if len(args.output_units) != 1:
            salir("Numero erroneo de salidas: {}".format(args.output_units))
    else:
        if len(args.input_units) != 8:
            salir("Numero erroneo de entradas: {}".format(args.input_units))
        if len(args.output_units) != 2:
            salir("Numero erroneo de salidas: {}".format(args.output_units))

    def parse_act_str(act_str):
        if act_str in ('sign', 's'):
            return af.sign()
        elif act_str in ('tanh', 't'):
            return af.tanh()
        elif act_str in ('sigmoid', 'l'):
            return af.sigmoid()
        elif act_str in ('ReLu', 'r'):
            return af.ReLu()
        else:
            return af.identity()

    ns = args.input_units + args.hidden_units + args.output_units

    gss = args.act_hidden_units + args.act_output_units
    gs = map(parse_act_str, gss)

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

    if not args.alpha and not args.a and not args.b:
        tutor = lm.BackPropagation(red)
        learn_funct = tutor.learn
    elif args.a or args.b:
        tutor = lm.BackPropagationOptimized(red)
        learn_funct = tutor.learn_adaptative
    else: # args.alpha:
        tutor = lm.BackPropagationOptimized(red)
        learn_funct = tutor.learn

    return {'training_db':TRAINING_DB[args.ej],
            'learn_funct': learn_funct,
            'tutor': training_db,
            'learn_params' : lear_params}


def experimentar(config):
    training, validation = load_training_validation(0.6)
    norm_funct = get_normalization_function(training)
    training = list(map(norm_funct, training))
    validation = list(map(norm_funct, training))

    red = config['red']
    learn_params = config['learn_params']
    print(red.ns)
    tutor = params['lc'](red)
    filename_base = DIR_EJ2_BASE
    filename_base += 'ex_{}-{}_red_{}'.format(str(i+1),str(j+1),"-".join(map(str, red.ns)))

    for epoch, error_training in tutor.learn(training,
                                             **learn_params):
        error_validation = red.error_training(validation)
        print("{}\t{}\t{}".format(epoch, \
                                  error_training, \
                                  error_validation))

def main():
    config = parse_argv()
    experimentar
