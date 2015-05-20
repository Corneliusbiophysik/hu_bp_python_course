import random
import sys

class BioMolecule(object):
    """
    A generic molecule that has basic attributes like id, name and
    mass.

    @type id: int
    @type name: str
    @type mass: float
    """
    def __init__(self, id, name, mass=None):
        #self._id = id
        self.id = id
        self.name = name
        self.mass = mass

    @property 
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value,str):
            raise TypeError("name ist kein string")
        self.__name = value

    @property
    def mass(self):
        return self.__mass

    @mass.setter
    def mass(self, value):
        if not isinstance(value, float):
            raise TypeError("masse ist kein Float")
        self.__mass = value

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self,value):
        if not isinstance(value, int):
            raise TypeError("id ist kein Integer")
        self.__id = value


    # 1. Write setter and getter methods for all attributes.
    #    Use @property decorators as dicussed in the lecture
    # 2. In the setter methods check for the type of each attribute.

class Polymer(BioMolecule):
    """
    A polymer molecule that has a sequence attribute which is
    accessible via indexing the object. 

    @type id: int
    @type name: str
    @type sequence: str
    @type mass: float
    """
    def __init__(self, id, name, sequence, mass=None):
        # 3. Initialize the parent class correctly
        super(Polymer, self).__init__(id,name,mass)
        self.sequence = sequence

    @property
    def sequence(self):
        return self.__sequence

    @sequence.setter
    def sequence(self,value):
        if not isinstance(value,str):
            raise TypeError("Sequenz ist kein String")
        self.__sequence = value       

    
    # 4. Write getter and setter for sequence, again check for type
    # 5. run in ipython, instantiate this class, and test it
    def __getitem__(self, value):
        """
        Makes the sequence accessible via the indexing operators:
<        p[10] returns the tenth character in the sequence.
        """
        return self.sequence[value]

    def __setitem__(self, key, value):
        """
         Enables changing of sequence characters via the indexing operators.       
        """
        self.sequence[key] = value


class MRNA(Polymer):
    def __init__(self, id, name, sequence, mass=None):
        super(MRNA, self).__init__(id,name,sequence,mass)
        # 6. Initialize the parent class correctly

        # 7. Create a list that stores if a ribosome is bound for each
        # codon (triplet).
        self.binding = [0 for i in range(len(sequence)/3)] # use this attribute for 7.
   
    def calculate_mass(self):
        NA_mass = {'A': 1.0, 'U': 2.2, 'G':2.1, 'C':1.3}
        m=0.
        for i in NA_mass.keys():
            m = m + NA_mass[i] * self.sequence.count(i,0,len(self.sequence))
        print m


