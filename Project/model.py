import processes as proc
import molecules as mol
import numpy as np
from Input.KnowledgeBase import KnowledgeBase as know

class Model(object):
    """
    Initializes the states and processes for the model and lets the processes update their corresponding states.
    """
    def __init__(self):
        self.states = {}
        self.processes = {}
        kb = know()
        genes = ['MG_001', 'MG_002', 'MG_003', 'MG_004', 'MG_005']
        print genes

        # initiate states
        self.ribosomes = {'Ribosomes': mol.Ribosome('Ribosomes', 'Ribosomes', 10)}
        self.mrnas = {'MRNA_{0}'.format(i): mol.MRNA(i, 'MRNA_{0}'.format(i), "UUUUUUUUUUAA") for i in genes}
        self.proteasomes = {'Proteasomes': mol.Proteasome('Proteasomes', 'Proteasomes', 10)}
        self.states.update(self.ribosomes)
        self.states.update(self.mrnas)
        self.states.update(self.proteasomes)

        # initiate processes
        translation = proc.Translation(1, "Translation")
        translation.set_states(self.mrnas.keys(), self.ribosomes.keys())
        self.degradation = proc.Degradation(2, "Degradation")
        self.processes = {"Translation":translation}


    def step(self):
        """
        Do one update step for each process.

        """
        for p in self.processes:
            self.processes[p].update(self)

            protein = []
            g = 0
            for x in self.states.keys():
                if "Protein_" in x:
                    protein.append(x)
                    g += len(self.states[x])
            self.degradation.set_states(protein, self.proteasomes.keys() )
            self.degradation.update(self)
            g = 0



    def simulate(self, steps, log=True):
        """
        Simulate the model for some time.

        """
        
        
        for s in xrange(steps):
            self.step()
            if log: # This could be an entry point for further logging
                # print count of each protein to the screen
                #print '\r{}'.format([len(self.states[x]) for x in self.states.keys() if "Protein_" in x]),
                pass
                

            
if __name__ == "__main__":
    c = Model()
    c.simulate(100, log=True)


