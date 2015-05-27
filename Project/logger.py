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
        


        def get_value(x):
            if isinstance(x,list):
                return len(x)
            if isinstance(x,mol.MRNA):
                if x.binding != [0]*(len(x.sequence)/3):
                    return 1
            if isinstance(x,mol.Ribosome):
                return x.count

        def set_attributes(i,x,t):
            if i in x:                
                result[i]['timecourse'][t]=get_value(x[i])#len(x[i])
                try:
                    result[i]['mass']=x[i].mass
                except: 
                    result[i]['mass']=None
                try:
                    result[i]['sequence']=x[i].sequence
                except: 
                    result[i]['sequence']=None

   
 

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



