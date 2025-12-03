#!/usr/bin/python

import numpy as np
import pyximport;pyximport.install(setup_args={
                              "include_dirs":np.get_include()},
                            reload_support=True)

import XOR_print_kbit

samples = 10000
X = np.random.random_integers(0,1,size=(samples,5)).astype(dtype=np.int32)
Y = np.zeros([samples]).astype(dtype=np.int32)



#######################
#NOISE FREE BELOW #####
#######################
for i in range(samples):
    # noise free configuration
    # if (X[i, :] == [1, 0, 1, 0, 1]).all(): # 10101 -> 1
    #     Y[i] = 1

    if (X[i, :4] == [1, 0, 1, 0]).all(): # 10101 or 10100 -> 1
        Y[i] = 1

#######################
#END: FREE BELOW #####
#######################





# Parameters for the Tsetlin Machine
number_of_clauses = 5
T = 2
s = 3.0
states = 100 # The state number of TA on each side of action (Include/Exclude). LJ
Th = 2


# Parameters of the pattern recognition problem. The number of input Boolean numbers, X. LJ
number_of_features = 5

# Training configuration
epochs = 1000

# Loading of training and test data
NoOfTrainingSamples = len(X)*80//100
NoOfTestingSamples = len(X) - NoOfTrainingSamples


X_training = X[0:NoOfTrainingSamples,:] # Input features
y_training = Y[0:NoOfTrainingSamples] # Target value

X_test = X[NoOfTrainingSamples:NoOfTrainingSamples+NoOfTestingSamples,:] # Input features
y_test = Y[NoOfTrainingSamples:NoOfTrainingSamples+NoOfTestingSamples] # Target value

# This is a multiclass variant of the Tsetlin Machine, capable of distinguishing between multiple classes
tsetlin_machine = XOR_print.TsetlinMachine(number_of_clauses, number_of_features, states, s, T, Th)

# Training of the Tsetlin Machine in batch mode. The Tsetlin Machine can also be trained online
tsetlin_machine.fit(X_training, y_training, y_training.shape[0], epochs=epochs)

# Some performacne statistics

print("Accuracy on test data:", tsetlin_machine.evaluate(X_test, y_test, y_test.shape[0]))

for clause in range(number_of_clauses):
    print('Clause', clause+1),
    for feature in range(number_of_features):
        for tatype in range(2):
            State = tsetlin_machine.get_state(clause,feature,tatype)
            if State >= states+1:
                Decision = 'In'
            else:
                Decision = 'Ex'
            print('feature %d TA %d State %d Decision %s' % (feature, tatype+1, State, Decision)),
    print('/n')