import molecules

class Logger(object):

    return_type={'mass': None
                  'sequence': None
                  'timecourse': None}

    def __init__(self):
        self.__temp_data=[]

    def __add__(self,x):
        self.__temp_data.append(x)

    def output(self):
        result = return_type

        for x in self.__temp_data:
            for y in x:
                #prüfen, ob Objekt Eigenschaft masse besitzt.
                #dann mass=masse von Objekt
                #ansonsten continue 

        return result



