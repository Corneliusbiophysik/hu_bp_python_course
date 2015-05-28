import processes as proc
import molecules as mol
from processes import Process
from molecules import BioMoleculeCount
from molecules import BioMolecule


class DNA(BioMolecule):
    def __init__(self, mid, name, length, mass=0):
        super(DNA, self).__init__(mid, name, mass)
        self._length=length

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value):
        self._length = value

class PolymeraseIII(BioMoleculeCount):
	#position=int; bound=boolean
    def __init__(self, mid, name, count=0, position=0, bound=False):
        super(PolymeraseIII, self).__init__(mid, name, count)
        self._position=position
        self._bound=bound

    @property
    def bound(self):
        return self._bound

    @bound.setter
    def bound(self, value):
        self._bound = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

class Helicase(BioMoleculeCount):
	#position=int; bound=boolean
    def __init__(self, mid, name, count=0, position=0, bound=False):
        super(Helicase, self).__init__(mid, name, count)
        self._position=position
        self._bound = bound

    @property
    def bound(self):
        return self._bound

    @bound.setter
    def bound(self, value):
        self._bound = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value


class Replication(Process):
    def __init__(self, id, name, double=False):
        super(Replication, self).__init__(id, name)
        self._double = double

    @property
    def double(self):
        return self._double

    @double.setter
    def double(self, value):
        self._double = value


    def update(self, model):
    	#return position helicase und polymeraseIII
        self.PolymeraseIII = model.states[self.enzyme_ids[0]]
        self.Helicase = model.states[self.enzyme_ids[1]]
        self.DNA = model.states[self.substrate_ids[0]]
        if self.double ==False:
            if self.PolymeraseIII.bound == False:
                self.initiate(DNA)
            elif self.Helicase.bound == True:
                self.elongate(DNA)
            else:
                self.terminate(DNA)


    def initiate(self, DNA):
    	#helicase wird aktiviert
        self.Helicase.bound =True
        self.Helicase.position += 100
        if self.Helicase.position ==1500: # 1500 ist Mindestabstand zwischen Helicase und PolyIII
            self.PolymeraseIII.bound = True


    def elongate(self,DNA):
    	#helicase und polyIII gehen weiter mit 100nt/s
        self.Helicase.position += 100
        self.PolymeraseIII.position += 100
        if self.Helicase.position >= self.DNA.length:
            self.Helicase.bound =False

    def terminate(self,DNA):
    	#wenn pos= length helicase + polyIII fallen ab, double true setzten
        self.PolymeraseIII.position += 100
        if self.PolymeraseIII.position >= self.DNA.length:
            self.PolymeraseIII.bound = False
            self.double = True