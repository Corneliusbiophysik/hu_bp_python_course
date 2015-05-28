import processes as proc
import molecules as mol
import replication as repl
import random

class Model(object):
    """
    Initializes the states and processes for the model and lets the processes update their corresponding states.
    """
    def __init__(self):
        self.states = {}
        self.processes = {}
        #initialisieren der Tabelle

        # initiate states
        self.ribosomes = {'Ribosomes': mol.Ribosome('Ribosomes', 'Ribosomes', 10)}
        self.mrnas = {'MRNA_{0}'.format(i): mol.MRNA(i, 'MRNA_{0}'.format(i), "UUUUUUUUUUAA") for i in xrange(50)}
        self.metabolites = {'ATP': mol.Metabolite(0, 'ATP', 6000.0), 'AA': mol.Metabolite(1, 'AA', 4000.0), 'NT': mol.Metabolite(2, 'NT', 2000.0)}#anpassen an Tabelle
        

        self.states.update(self.ribosomes)
        self.states.update(self.mrnas)
        self.states.update(self.metabolites)

        # initiate processes
        translation = proc.Translation(1, "Translation")
        translation.set_states(self.mrnas.keys() + self.metabolites.keys(), self.ribosomes.keys() )
        self.processes = {"Translation":translation}

        #replication = repl.Replication(2, "Replication")
        #replication.set_states(self.mrnas.keys() + self.metabolites.keys(), self.ribosomes.keys() )
        #self.processes = {"Translation":translation, "Replication":replication}

    def step(self):

        
        """
        Do one update step for each process.

        """

        #print("Current ATP:{}".format(self.states["ATP"].count))
        #print("Current AA:{}".format(self.states["AA"].count))
        keys = self.processes.keys()
        random.shuffle(keys)
        for p in keys:
            
            self.processes[p].update(self)

    def simulate(self, steps, log=True):
        """
        Simulate the model for some time.

        """
        for s in xrange(steps):
            self.step()
            if log: # This could be an entry point for further logging
                # print count of each protein to the screen
                print '\r{}'.format([len(self.states[x]) for x in self.states.keys() if "Protein_" in x]),
            
if __name__ == "__main__":
    c = Model()
    c.simulate(100, log=True)
