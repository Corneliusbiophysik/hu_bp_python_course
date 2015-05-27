import molecules as mol
import numpy as np
import copy
import pickle
class Logger(object):

    def __init__(self):
        self.__temp_data=[] # Array (length = time) of dictionary(keys = states): 


    def add_step(self,x):
        self.__temp_data.append(dict(copy.deepcopy(x)))

    def output(self):

        def get_keys():
            for i in self.__temp_data:
                for key in i.keys():
                    set_of_keys.add(key)

        def init_result():
            temp = {'mass': None,
                    'sequence': None,
                    'timecourse': np.zeros(N)}

            for i in set_of_keys:
                result[i]=copy.deepcopy(temp)
        


        def get_value(state):               # Gebe einen sinnvollen Wert aus, der sich nach der Art des Biomolekuels richtet
            if isinstance(state,list):
                return len(state)
            if isinstance(state,mol.MRNA):
                if state.binding != [0]*(len(state.sequence)/3):
                    return 1
            if isinstance(state,mol.Ribosome):
                return state.count

        def set_attributes(key_of_state,states_at_timepoint,t):
            if key_of_state in states_at_timepoint:                
                result[key_of_state]['timecourse'][t]=get_value(states_at_timepoint[key_of_state])#len(states_at_timepoint[i])
                try:
                    result[key_of_state]['mass']=states_at_timepoint[key_of_state].mass
                except: 
                    result[key_of_state]['mass']=None
                try:
                    result[key_of_state]['sequence']=states_at_timepoint[key_of_state].sequence
                except: 
                    result[key_of_state]['sequence']=None

   
 

        N = len(self.__temp_data)     
        set_of_keys=set()        
        get_keys()    # alle State keys einsammeln
        result = {} 
        init_result() # Ausgabe vorbereiten

        for t in xrange(N):
            for i in set_of_keys:
                set_attributes(i,self.__temp_data[t],t)

        with open('output.p','wb') as f:
            pickle.dump(result,f)
        return result



