import molecules as mol
import replication as rep
import numpy as np
import copy
import pickle

class Logger(object):
    """
    Collects all the states of a timestep and stores these statevectors in a list as a property of the Logger object.
    The collected data is converted via the output-method to generate a dictionary of dictionaries.
    The first Layer of dictionaries is equal to the states.
    The second Layer of dictionaries combines different Properties of a state (e.g.: mass, sequence) and 
    a timecourse for a characteristic value of the state (e.g.: number of molecules, concentration)   
    """

    def __init__(self):
        self.__temp_data=[] # Array (length = time) of dictionary(keys = states). used  


    def add_step(self,x):
        self.__temp_data.append(dict(copy.deepcopy(x)))
        #self.__temp_data.append(dict(x))


    def output(self):

        def get_keys():                     # make a set of all keys, which occured during the simulation
            for i in self.__temp_data:
                for key in i.keys():
                    set_of_keys.add(key)

        def init_result():                  # initialise the output datatype
            temp = {'mass': None,
                    'sequence': None,
                    'timecourse': np.zeros(N)}

            for i in set_of_keys:
                result[i]=copy.deepcopy(temp)
        


        def get_value(state):               # return a characteristic value (to create a y-value for the timecourse),
            if isinstance(state,list):      # the nature of this value depends on the Class of the state object
                return len(state)
            if isinstance(state,mol.MRNA):
                if state.binding != [0]*(len(state.sequence)/3):
                    return 1
            if isinstance(state,mol.Ribosome):
                return state.count
            if isinstance(state,rep.DNA):
                return state.nucleotides
            if isinstance(state,rep.PolymeraseIII):
                return state.position

        def set_attributes(key_of_state,states_at_timepoint,t): # set the properties and timecourse in the second layer of dictionarie of the ouput data type
            if key_of_state in states_at_timepoint:                
                result[key_of_state]['timecourse'][t]=get_value(states_at_timepoint[key_of_state]) 
                try:
                    result[key_of_state]['mass']=states_at_timepoint[key_of_state].mass
                except: 
                    result[key_of_state]['mass']=None
                try:
                    result[key_of_state]['sequence']=states_at_timepoint[key_of_state].sequence
                except: 
                    result[key_of_state]['sequence']=None  
 
        N = len(self.__temp_data)   # number of timesteps that where recorded   
        set_of_keys=set()           # make set of keys
        get_keys()                  
        result = {}                 # prepare output 
        init_result()               

        for t in xrange(N):         # convert: collected data -> output data type
            for i in set_of_keys:
                set_attributes(i,self.__temp_data[t],t)

        # with open('output.p','wb') as f: 
        #     pickle.dump(result,f)
        return result



