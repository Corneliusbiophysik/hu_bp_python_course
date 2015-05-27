import molecules
import numpy as np

import copy
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
                    'timecourse': range(100)}#np.zeros(100)}

            for i in set_of_keys:
                result[i]=copy.deepcopy(temp)
        


        def get_count(x):
            if isinstance(x,list):
                return len(x)

            return 0
            # else:
            #     try:
            #         return x.count
            #     except:
            #         return None

        def set_attributes(i,x,t):
            if i in x[t]:
                #pass
                #print i#,result[i]['timecourse']   
                #print i 
                #print t, len(x[t])          
                result[i]['timecourse'][t]=''+ i
                try:
                    result[i]['mass']=x[t][i].mass
                except: 
                    result[i]['mass']=None
                try:
                    result[i]['sequence']=x[t][i].sequence
                except: 
                    result[i]['sequence']=None

   
 

              
        set_of_keys=set()        
        get_keys()    # alle State keys einsammeln
        result = {} 
        init_result() # Ausgabe vorbereiten
        #print result
        #print self.__temp_data[0],len(self.__temp_data[0])
        for t in xrange(10):
            for i in set_of_keys:
            #for t in xrange(100):
                #print i
                set_attributes(i,self.__temp_data,t)

        print result
        #print result['MRNA3']









        #print set_of_keys








        
        #print self.__temp_data
        # for t in xrange(100):
        #     for y in set_of_keys :
        #         set_attributes(result[y],self.__temp_data[99][y],99)

        return None#result



