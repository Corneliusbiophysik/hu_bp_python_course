import molecules
import numpy as np

class Logger(object):

    def __init__(self):
        self.__temp_data=[] # Array (length = time) of dictionary(keys = states): 


    def add_step(self,x):
        self.__temp_data.append(dict(x))

    def output(self):

        def get_count(x):
            if isinstance(x,list):
                return len(x)
            else:
                try:
                    return x.count
                except:
                    return None

        def set_attributes(element,x,t):
            try:
                element['mass']=x.mass
            except: 
                element['mass']=None
            try:
                element['sequence']=x.sequence
            except: 
                element['sequence']=None
            try:
                element['timecourse'][t]=get_count(x)
            except:
                element['timecourse'][t]=None


        set_of_keys=self.__temp_data[99].keys()


        temp = {'mass': None,
                'sequence': None,
                'timecourse': np.zeros(100)}

        result = {}
        for i in set_of_keys:
            #print i
            result[i]=temp.copy()
        
        #print self.__temp_data
        for t in xrange(100):
            for y in set_of_keys :
                set_attributes(result[y],self.__temp_data[99][y],99)
                #result[y]=element       
            
            #     #continue
            #     #prufen, ob Objekt Eigenschaft masse besitzt.
            #     #dann mass=masse von Objekt
            #     #ansonsten continue 
        return result



