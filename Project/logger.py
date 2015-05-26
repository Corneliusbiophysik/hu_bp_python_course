import molecules

class Logger(object):

    def __init__(self):
        self.__temp_data=[] # Array (length = time) of dictionary(keys = states): 


    def add_step(self,x):
        self.__temp_data.append(dict(x))

    def output(self):
        element = {'mass': None,
                   'sequence': None,
                   'timecourse': None}
        result = {}
        #print self.__temp_data
        for y in self.__temp_data[99].keys():
            temp = element.copy()
            #print y
            try:
                temp['mass']=self.__temp_data[99][y].mass
            except: 
                temp['mass']=None
            try:
                temp['sequence']=self.__temp_data[99][y].sequence
            except: 
                temp['sequence']=None
        
            result[y]=temp
            #     #continue
            #     #prufen, ob Objekt Eigenschaft masse besitzt.
            #     #dann mass=masse von Objekt
            #     #ansonsten continue 
        return result



