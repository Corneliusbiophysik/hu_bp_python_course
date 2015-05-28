import random 
import numpy.random as nr
import processes as proc
import molecules as mol
from processes import Process
from molecules import BioMoleculeCount
from molecules import BioMolecule


class DNA(BioMolecule):
    def __init__(self, mid, name, length, mass=0):
        super(DNA, self).__init__(mid, name, mass)
        self._length=length/2

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

    def __init__(self, id, name, ATP, NT, double=False):
        super(Replication, self).__init__(id, name)
        self._double = double
        self.ATP_molecules = ATP
        self.Nucleotide = NT

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
        if self.Helicase.bound == False:
            x_number =nr.randint(1,10)
            if x_number ==1:
                self.Helicase.bound =True
                #if self.ATP_molecules >= 100 and (self.Helicase.position - self.PolymeraseIII.position) < 3000:
                #    self.Helicase.position += 100
                #    self.ATP_molecules -= 100
        elif self.ATP_molecules >= 200 and (self.Helicase.position - self.PolymeraseIII.position) < 3000:
            self.Helicase.position += 100
            self.ATP_molecules -= 200
        elif self.ATP_molecules > 0 and (self.Helicase.position - self.PolymeraseIII.position) < 3000:
            self.Helicase.position += ATP_molecules/2
            ATP_molecules -= 2*(ATP_molecules/2)
        if self.Helicase.position >=1500: # 1500 ist Mindestabstand zwischen Helicase und PolyIII
            y_number =nr.randint(1,5)
            if y_number ==1:
                self.PolymeraseIII.bound = True
        if self.Helicase.position > self.DNA.length:
            self.ATP_molecules=self.ATP_molecules+(self.Helicase.position -self.DNA.length)
            self.Helicase.position = self.DNA.length


    def elongate(self,DNA):
    	#helicase und polyIII gehen weiter mit 100nt/s
        if self.ATP_molecules >= 200 and (self.Helicase.position - self.PolymeraseIII.position) < 3000: #genug ATP, Abstand klein genug
            self.Helicase.position += 100 
            self.ATP_molecules -= 200
            if self.Nucleotide >= 400 and (self.Helicase.position - self.PolymeraseIII.position) > 1500: #genug  Nucleotide (>=200)
                self.PolymeraseIII.position += 100
                self.Nucleotide -= 400
            elif self.Nucleotide > 3 and (self.Helicase.position - self.PolymeraseIII.position) > 1500: #nicht genug Nucleotide (1-199)
                self.PolymeraseIII.position += self.Nucleotide/4
                self.Helicase.position = self.Helicase.position -100 +self.Nucleotide/4
                self.ATP_molecules =self.ATP_molecules+200-self.Nucleotide/2
                self.Nucleotide -= 4*(self.Nucleotide/4)
        
        elif self.ATP_molecules >= 0 and (self.Helicase.position - self.PolymeraseIII.position) < 3000: #nicht genug ATP, Abstand klein genug
            self.Helicase.position += self.ATP_molecules
            if self.Nucleotide >= 400 and (self.Helicase.position - self.PolymeraseIII.position) > 1500:  #genug Nucleotide
                self.PolymeraseIII.position += 100
                self.Nucleotide -= 400
            elif self.Nucleotide > 1 and (self.Helicase.position - self.PolymeraseIII.position) > 1500: #nicht genug Nucleotide
                self.PolymeraseIII.position += self.Nucleotide/4
                self.Helicase.position = self.Helicase.position -self.ATP_molecules +self.Nucleotide/4
                self.ATP_molecules -=self.Nucleotide/2
                self.Nucleotide -= 4*(self.Nucleotide/4)
            self.ATP_molecules -= self.ATP_molecules

        if self.Helicase.position > self.DNA.length:
            self.ATP_molecules=self.ATP_molecules+(self.Helicase.position -self.DNA.length)
            self.Helicase.position = self.DNA.length

        if self.Helicase.position >= self.DNA.length:
            self.Helicase.bound =False
        print ('ATP:',self.ATP_molecules,'NT:',self.Nucleotide)

    def terminate(self,DNA):
    	#wenn pos= length helicase + polyIII fallen ab, double true setzten
        if self.Nucleotide >= 400:
            self.PolymeraseIII.position += 200
            self.Nucleotide -= 400
        elif self.Nucleotide>1:
            self.PolymeraseIII.position += self.Nucleotide/4
            self.Nucleotide -= 4*self.Nucleotide/4
        if self.PolymeraseIII.position >= self.DNA.length:
            self.PolymeraseIII.bound = False
            self.double = True
