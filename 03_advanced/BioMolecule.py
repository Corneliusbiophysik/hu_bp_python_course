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
        self.__id = id
        self.name = name
        self.mass = mass

    @property
    def mass(self):
        return self.__mass

    @mass.setter
    def mass(self, value):
        if not isinstance(value, float):
            raise TypeError('Mass must be integer.')
        self.__mass = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, word):
        if not isinstance(word, str):
            raise TypeError('Mass must be string.')
        self.__name = word

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, number):
        if not isinstance(number, int):
            raise TypeError('ID must be integer.')
        self.__id = number

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
    def __init__(self, id, sequence, name, mass=None):
        super(Polymer, self).__init__(id, name, mass)
        # 3. Initialize the parent class correctly
        self.__sequence = sequence

    @property
    def sequence(self):
        return self.__sequence

    @sequence.setter
    def sequence(self, words):
        if not isinstance(words, str):
            raise TypeError('Sequence must be string.')
        self.__sequence = words


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
    def __init__(self, id, sequence, name, mass=None):
        super(MRNA, self).__init__(id, sequence, name, mass)
        # 6. Initialize the parent class correctly

        # 7. Create a list that stores if a ribosome is bound for each
        # codon (triplet).
        self.binding = [] # use this attribute for 7.