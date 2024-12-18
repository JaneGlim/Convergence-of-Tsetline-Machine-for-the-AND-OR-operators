#cython: boundscheck=False, cdivision=True, initializedcheck=False, nonecheck=False

import numpy as np
cimport numpy as np
import random
from libc.stdlib cimport rand, RAND_MAX

#############################
### The Tsetlin Machine #####
#############################

cdef class TsetlinMachine:
    cdef int number_of_clauses
    cdef int number_of_features
    
    cdef float s
    cdef int number_of_states
    cdef int threshold
    cdef int Th

    cdef int[:,:,:] ta_state
    
    cdef int[:] clause_sign

    cdef int[:] clause_output

    cdef int[:] feedback_to_clauses
    cdef int noofupdates

    # Initialization of the Tsetlin Machine
    def __init__(self, number_of_clauses, number_of_features, number_of_states, s, threshold, Th):
        cdef int j

        self.number_of_clauses = number_of_clauses
        self.number_of_features = number_of_features
        self.number_of_states = number_of_states
        self.s = s
        self.threshold = threshold
        self.Th = Th

        # The state of each Tsetlin Automaton is stored here. The automata are randomly initialized to either 'number_of_states' or 'number_of_states' + 1.
        self.ta_state = np.random.choice([self.number_of_states, self.number_of_states+1], size=(self.number_of_clauses, self.number_of_features, 2)).astype(dtype=np.int32)

        # Data structure for keeping track of the sign of each clause
        self.clause_sign = np.zeros(self.number_of_clauses, dtype=np.int32)
        
        # Data structures for intermediate calculations (clause output, summation of votes, and feedback to clauses)
        self.clause_output = np.zeros(shape=(self.number_of_clauses), dtype=np.int32)
        self.feedback_to_clauses = np.zeros(shape=(self.number_of_clauses), dtype=np.int32)

        # Set up the Tsetlin Machine structure
        for j in xrange(self.number_of_clauses):
            if j % 2 == 0:
                self.clause_sign[j] = 1
            else:
                self.clause_sign[j] = 1


    # Calculate the output of each clause using the actions of each Tsetline Automaton.
    # Output is stored an internal output array. 
    # We need to handle the value of empty clause. It is different for training and testing. We must specify. LJ 18/11/2024
    cdef void calculate_clause_output(self, int[:] X, train):
        cdef int j, k, num_ex

        if train == True:
            for j in xrange(self.number_of_clauses):
                self.clause_output[j] = 1
                for k in xrange(self.number_of_features):
                    action_include = self.action(self.ta_state[j,k,0])
                    action_include_negated = self.action(self.ta_state[j,k,1])
    
                    if (action_include == 1 and X[k] == 0) or (action_include_negated == 1 and X[k] == 1):
                        self.clause_output[j] = 0
                        break
                    
        if train == False:
            for j in xrange(self.number_of_clauses):
                self.clause_output[j] = 1
                num_ex = 0
                for k in xrange(self.number_of_features):
                    action_include = self.action(self.ta_state[j,k,0])
                    action_include_negated = self.action(self.ta_state[j,k,1])
                    if action_include == 1 or action_include_negated == 1:
                        num_ex += 1
    
                    if (action_include == 1 and X[k] == 0) or (action_include_negated == 1 and X[k] == 1):
                        self.clause_output[j] = 0
                   
                if num_ex == 0:
                    self.clause_output[j] = 0                 

                    
    
    ###########################################
    ### Predict Target Output y for Input X ###
    ###########################################

    cpdef int predict(self, int[:] X):
        cdef int output_sum
        cdef int j
        
        ###############################
        ### Calculate Clause Output ###
        ###############################

        self.calculate_clause_output(X, train=False)

        ###########################
        ### Sum up Clause Votes ###
        ###########################b

        output_sum = self.sum_up_clause_votes()

        if output_sum >= self.Th:
            return 1
        else:
            return 0

    # Translates automata state to action 
    cdef int action(self, int state):
        if state <= self.number_of_states:
            return 0
        else:
            return 1

    # Get the state of a specific automaton, indexed by clause, feature, and automaton type (include/include negated).
    def get_state(self, int clause, int feature, int automaton_type):
        return self.ta_state[clause,feature,automaton_type]

    # Sum up the votes for each output decision (y=0 or y = 1)
    cdef int sum_up_clause_votes(self):
        cdef int output_sum
        cdef int j

        output_sum = 0
        for j in xrange(self.number_of_clauses):
            output_sum += self.clause_output[j]*self.clause_sign[j]
        
        if output_sum > self.threshold:
            output_sum = self.threshold
        
        elif output_sum < self.Th:
            output_sum = 0

        return output_sum

    ############################################
    ### Evaluate the Trained Tsetlin Machine ###
    ############################################

    def evaluate(self, int[:,:] X, int[:] y, int number_of_examples):
        cdef int j,l
        cdef int errors
        cdef int output_sum
        cdef int[:] Xi

        Xi = np.zeros((self.number_of_features,), dtype=np.int32)

        errors = 0
        for l in xrange(number_of_examples):
            ###############################
            ### Calculate Clause Output ###
            ###############################

            for j in xrange(self.number_of_features):
                Xi[j] = X[l,j]

            self.calculate_clause_output(Xi, train=False)

            ###########################
            ### Sum up Clause Votes ###
            ###########################

            output_sum = self.sum_up_clause_votes()
            
            if output_sum >= self.Th and y[l] == 0:
                errors += 1

            elif output_sum < self.Th and y[l] == 1:
                errors += 1

        return 1.0 - 1.0 * errors / number_of_examples

    ##########################################
    ### Online Training of Tsetlin Machine ###
    ##########################################

    # The Tsetlin Machine can be trained incrementally, one training example at a time.
    # Use this method directly for online and incremental training.

    cpdef void update(self, int[:] X, int y):
        cdef int i, j
        cdef int action_include, action_include_negated
        cdef int output_sum

        ###############################
        ### Calculate Clause Output ###
        ###############################

        self.calculate_clause_output(X, train=True)

        ###########################
        ### Sum up Clause Votes ###
        ###########################

        output_sum = self.sum_up_clause_votes()

        #####################################
        ### Calculate Feedback to Clauses ###
        #####################################

        # Initialize feedback to clauses
        for j in xrange(self.number_of_clauses):
            self.feedback_to_clauses[j] = 0

        if y == 1:
            # Calculate feedback to clauses
            for j in xrange(self.number_of_clauses):
                if 1.0*rand()/RAND_MAX >= 1.0*(self.threshold - output_sum)/(2*self.threshold):
                    continue

                if self.clause_sign[j] > 0:
                    # Type I Feedback                
                    self.feedback_to_clauses[j] += 1

        elif y == 0:
            for j in xrange(self.number_of_clauses):
                if 1.0*rand()/RAND_MAX >= 1.0*(self.threshold + output_sum)/(2*self.threshold):
                    continue

                if self.clause_sign[j] > 0:
                    # Type II Feedback
                    self.feedback_to_clauses[j] -= 1

    
        for j in xrange(self.number_of_clauses):
            if self.feedback_to_clauses[j] > 0:
                #######################################################
                ### Type I Feedback (Combats False Negative Output) ###
                #######################################################

                if self.clause_output[j] == 0:        
                    for k in xrange(self.number_of_features):    
                        if 1.0*rand()/RAND_MAX <= 1.0/self.s:                                
                            if self.ta_state[j,k,0] > 1:
                                self.ta_state[j,k,0] -= 1
                                self.noofupdates += 1
                                                    
                        if 1.0*rand()/RAND_MAX <= 1.0/self.s:
                            if self.ta_state[j,k,1] > 1:
                                self.ta_state[j,k,1] -= 1
                                self.noofupdates += 1

                if self.clause_output[j] == 1:                    
                    for k in xrange(self.number_of_features):
                        if X[k] == 1:
                            if 1.0*rand()/RAND_MAX <= 1.0*(self.s-1)/self.s:
                                if self.ta_state[j,k,0] < self.number_of_states*2:
                                    self.ta_state[j,k,0] += 1
                                    self.noofupdates += 1

                            if 1.0*rand()/RAND_MAX <= 1.0/self.s:
                                if self.ta_state[j,k,1] > 1:
                                    self.ta_state[j,k,1] -= 1
                                    self.noofupdates += 1

                        elif X[k] == 0:
                            if 1.0*rand()/RAND_MAX <= 1.0*(self.s-1)/self.s:
                                if self.ta_state[j,k,1] < self.number_of_states*2:
                                    self.ta_state[j,k,1] += 1
                                    self.noofupdates += 1

                            if 1.0*rand()/RAND_MAX <= 1.0/self.s:
                                if self.ta_state[j,k,0] > 1:
                                    self.ta_state[j,k,0] -= 1
                                    self.noofupdates += 1
                    
            elif self.feedback_to_clauses[j] < 0:
                ########################################################
                ### Type II Feedback (Combats False Positive Output) ###
                ########################################################
                if self.clause_output[j] == 1:
                    for k in xrange(self.number_of_features):
                        action_include = self.action(self.ta_state[j,k,0])
                        action_include_negated = self.action(self.ta_state[j,k,1])

                        if X[k] == 0:
                            if action_include == 0 and self.ta_state[j,k,0] < self.number_of_states*2:
                                self.ta_state[j,k,0] += 1
                                self.noofupdates += 1
                                
                        elif X[k] == 1:
                            if action_include_negated == 0 and self.ta_state[j,k,1] < self.number_of_states*2:
                                self.ta_state[j,k,1] += 1
                                self.noofupdates += 1

    ##############################################
    ### Batch Mode Training of Tsetlin Machine ###
    ##############################################

    def fit(self, int[:,:] X, int[:] y, int number_of_examples, int epochs=100):
        cdef int j, l, epoch
        cdef int example_id
        cdef int target_class
        cdef int[:] Xi
        cdef long[:] random_index
        cdef int[:,:] ClauseOuts
        
        ClauseOuts = np.zeros(((self.number_of_clauses*self.number_of_features*2)+1, epochs), dtype=np.int32)
                
        Xi = np.zeros((self.number_of_features,), dtype=np.int32)
        
        random_index = np.arange(number_of_examples)

        for epoch in xrange(epochs):    
            #np.random.shuffle(random_index)
            self.noofupdates = 0

            for l in xrange(number_of_examples):
                example_id = random_index[l]
                target_class = y[example_id]

                for j in xrange(self.number_of_features):
                    Xi[j] = X[example_id,j]
                self.update(Xi, target_class)
                
            print_index = 0
            for clauseindex in range(self.number_of_clauses):
                for feature_index in [0,1]:
                    for feature_type in [0,1]: # 0 original, 1 negated
                        ClauseOuts[print_index,epoch] = self.ta_state[clauseindex, feature_index, feature_type] # It includes the states of TAs, Clause number times feature number times 2. LJ 
                        print_index += 1
                
            ClauseOuts[print_index,epoch] = self.noofupdates #the last colunm is the number of updates among all TAs. LJ
                
        import xlsxwriter        
        workbooko = xlsxwriter.Workbook('Case OR Clause out per epoch T=2.xlsx')
        worksheet = workbooko.add_worksheet() 
        row = 0
        for col, data in enumerate(ClauseOuts):
            worksheet.write_column(row, col, data)
        workbooko.close()
                
        return
