#!/usr/bin/python

import numpy as np
import pyximport; pyximport.install(setup_args={
                              "include_dirs":np.get_include()},
                            reload_support=True)

import XOR_print

samples = 5000
X = np.random.random_integers(0,1,size=(samples,2)).astype(dtype=np.int32)
Y = np.ones([samples]).astype(dtype=np.int32) 
samples_test = 2000


#################################
#Noisy with Wrong lable #########
#################################

noise_rate = 0.9

#noise confirguration: XOR with noise as (0 1 output 0) and (1 0 output 0)







#################################
# #noise confirguration: OR with noise as (0 0 output 1) 
# for i in range(samples):
#     if X[i, 0] == 0 and X[i, 1] == 0: 
#         if np.random.rand() >= noise_rate:
#             Y[i] = 0
#         else:
#             Y[i] = 1        
#################################






###########################################################
#noise confirguration: OR with noise as (1 1 output 0) and (0 1 output 0) and (1 0 output 0)
# for i in range(samples):
#     if X[i, 0] == 0 and X[i, 1] == 0: 
#        Y[i] = 0
# for i in range(samples):
#     if X[i, 0] == 0 and X[i, 1] == 1:
#         if np.random.rand() >= noise_rate:
#             Y[i] = 1
#         else:
#             Y[i] = 0
# for i in range(samples):
#     if X[i, 0] == 1 and X[i, 1] == 1:
#         if np.random.rand() >= noise_rate:
#             Y[i] = 1
#         else:
#             Y[i] = 0

# for i in range(samples):
#     if X[i, 0] == 1 and X[i, 1] == 0:
#         if np.random.rand() >= noise_rate:
#             Y[i] = 1
#         else:
#             Y[i] = 0
#########################################################




#########################################################
#noise confirguration: AND with noise as (0 0 output 1) and (1 1 output 0) and (0 1 output 1)
# for i in range(samples):
#     if X[i, 0] == 0 or X[i, 1] == 0: # AND
#        Y[i] = 0
# for i in range(samples):
#     if X[i, 0] == 0 and X[i, 1] == 0:
#         if np.random.rand() >= noise_rate:
#             Y[i] = 0
#         else:
#             Y[i] = 1
# for i in range(samples):
#     if X[i, 0] == 1 and X[i, 1] == 1:
#         if np.random.rand() >= noise_rate:
#             Y[i] = 1
#         else:
#             Y[i] = 0

# for i in range(samples):
#     if X[i, 0] == 0 and X[i, 1] == 1:
#         if np.random.rand() >= noise_rate:
#             Y[i] = 0
#         else:
#             Y[i] = 1
########################################################



#########################################################
#noise confirguration: AND with noise as 0 0 output 1
# for i in range(samples):
#     if X[i, 0] == 0 or X[i, 1] == 0: # AND
#        Y[i] = 0
# for i in range(samples):
#     if X[i, 0] == 0 and X[i, 1] == 0:
#         if np.random.rand() >= noise_rate:
#             Y[i] = 0
#         else:
#             Y[i] = 1
#########################################################





########################################################
#noise confirguration: AND with noise as 0 1 output 1
for i in range(samples):
    if X[i, 0] == 0 or X[i, 1] == 0: # AND
       Y[i] = 0
for i in range(samples):
    if X[i, 0] == 0 and X[i, 1] == 1:
        if np.random.rand() >= noise_rate:
            Y[i] = 0
        else:
            Y[i] = 1
#########################################################




########################################################    
#noise confirguration: AND with noise as 1 1 output 0
# for i in range(samples):
#     if X[i, 0] == 0 or X[i, 1] == 0: # AND
#        Y[i] = 0
#     if X[i, 0] == 1 and X[i, 1] == 1:
#        if np.random.rand() >= noise_rate: 
#            Y[i] = 1
#        else: # noise
#            Y[i] = 0
########################################################


###########################################################
#noise confirguration: XOR with noise as  (0 1 output 0) 
# for i in range(samples):
#     if X[i, 0] == 0 and X[i, 1] == 0: 
#        Y[i] = 0
# for i in range(samples):
#     if X[i, 0] == 0 and X[i, 1] == 1:
#         if np.random.rand() >= noise_rate:
#             Y[i] = 1
#         else:
#             Y[i] = 0
# for i in range(samples):
#     if X[i, 0] == 1 and X[i, 1] == 1:
#             Y[i] = 0

# for i in range(samples):
#     if X[i, 0] == 1 and X[i, 1] == 0:
#              Y[i] = 1
#########################################################





#################################
#END: Noisy with Wrong lable #########
#################################



#################################
# #test samples OR (no noise)
# X_or = np.random.random_integers(0,1,size=(samples_test,2)).astype(dtype=np.int32)
# Y_or = np.ones([samples_test]).astype(dtype=np.int32) #or
# for i in range(samples_test):
#     if X_or[i, 0] == 0 and X_or[i, 1] == 0:
#         Y_or[i] = 0
#################################

#################################
#test samples AND (no noise)
X_and = np.random.random_integers(0,1,size=(samples_test,2)).astype(dtype=np.int32)
Y_and = np.zeros([samples_test]).astype(dtype=np.int32) #AND
for i in range(samples_test):
    if X_and[i, 0] == 1 and X_and[i, 1] == 1:
        Y_and[i] = 1
###########################################################

#################################
# test samples XOR (no noise)
# X_xor = np.random.random_integers(0,1,size=(samples_test,2)).astype(dtype=np.int32)
# Y_xor = np.zeros([samples_test]).astype(dtype=np.int32) #xor
# for i in range(samples_test):
#     if X_xor[i, 0] == 1 or X_xor[i, 1] == 1:
#         Y_xor[i] = 1
#     if X_xor[i, 0] == 1 and X_xor[i, 1] == 1:
#         Y_xor[i] = 0
###########################################################



# Parameters for the Tsetlin Machine

T = 3
s = 3.0
number_of_clauses = 7
states = 100 # The state number of TA on each side of action (Include/Exclude). LJ
Th = 2


# Parameters of the pattern recognition problem. The number of input Boolean numbers, X. LJ
number_of_features = 2

# Training configuration
epochs = 1000

# Loading of training and test data
NoOfTrainingSamples = len(X)*80//100
NoOfTestingSamples = len(X) - NoOfTrainingSamples


X_training = X[0:NoOfTrainingSamples,:] # Input features
y_training = Y[0:NoOfTrainingSamples] # Target value

# remember to change it to the corresponding test samples. 
X_test = X_and
y_test = Y_and

#X_test = X[NoOfTrainingSamples:NoOfTrainingSamples+NoOfTestingSamples,:] # Input features
#y_test = Y[NoOfTrainingSamples:NoOfTrainingSamples+NoOfTestingSamples] # Target value

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