import molecules
import numpy as np

class Logger(object):

    def __init__(self):
        self.__temp_data=[] # Array (length = time) of dictionary(keys = states): 


    def add_step(self,x):
        self.__temp_data.append(dict(x))

    def output(self):

        def get_keys():
            for i in self.__temp_data:
                #sprint i.keys()
                for key in i.keys():
                    set_of_keys.add(key)

        def init_result():
            temp = {'mass': None,
                    'sequence': None,
                    'timecourse': np.zeros(100)}

            for i in set_of_keys:
                result[i]=temp.copy()
        


        def get_count(x):
            if isinstance(x,list):
                return len(x)
            else:
                try:
                    return x.count
                except:
                    return None

        def set_attributes(i,x,t):
            if i in x:
                element=result[i]
                try:
                    element['mass']=x[i].mass
                except: 
                    element['mass']=None
                try:
                    element['sequence']=x[i].sequence
                except: 
                    element['sequence']=None
                try:
                    element['timecourse'][t]=get_count(x)
                except:
                    element['timecourse'][t]=None

              
        set_of_keys=set()        
        get_keys()    # alle States einsammel
        result = {} 
        init_result() # Ausgabe vorbereiten

        for t in xrange(100):
            for i in set_of_keys:
                set_attributes(i,self.__temp_data[t],t)









        #print set_of_keys








        
        #print self.__temp_data
        # for t in xrange(100):
        #     for y in set_of_keys :
        #         set_attributes(result[y],self.__temp_data[99][y],99)

        return result



