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
        self._id = id
        self.name = name
        self.mass = mass

    # 1. Write setter and getter methods for all attributes.
    #    Use @property decorators as dicussed in the lecture
    # 2. In the setter methods check for the type of each attribute.

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
    	if not isinstance(value, int):
    		raise TypeError("Please enter integer")
    	self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, named):
    	if not isinstance(named, str):
    		raise TypeError("Please enter string")
    	self._name = named

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, ma):
    	if not isinstance(ma, float):
    		raise TypeError("Please enter float")
    	self._mass = ma

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
        super(Polymer, self).__init__(id, name, mass)
        self._sequence = sequence
        

    @property
    def sequence(self):
        return self._sequence

    @sequence.setter
    def sequence(self, seq):
        if not isinstance(seq, str):
            raise TypreError("Please enter string")
        self._sequence = seq
    
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
        # 6. Initialize the parent class correctly
        super(Polymer, self).__init__(id, name, mass)
        self._sequence = sequence

        # 7. Create a list that stores if a ribosome is bound for each
        # codon (triplet).
        length = sequence % 3

        self.binding = [range(length)] # use this attribute for 7.

    def calculate_mass(self):
        NA_mass = {'A': 1.0, 'U': 2.2, 'G':2.1, 'C':1.3}
        # 8. calculate the mass for the whole sequence
