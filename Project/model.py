import processes as proc
import molecules as mol
import logger as loggy
import visualization as vis
import replication as rep
import random
import Input.KnowledgeBase as know

class Model(object):
    """
    Initializes the states and processes for the model and lets the processes update their corresponding states.
    """
    def __init__(self):
        self.states = {}
        self.processes = {}


        DNA_length=580000
        ATP_mol=600000
        NT_mol=1400000
        kb = know.KnowledgeBase()
        genes = ['MG_001', 'MG_002', 'MG_003', 'MG_004', 'MG_005']


        # initiate states
        self.ribosomes = {'Ribosomes': mol.Ribosome('Ribosomes', 'Ribosomes', 10)}
        self.mrnas = {'MRNA_{0}'.format(i): mol.MRNA(i, 'MRNA_{0}'.format(i), "UUUUUUUUUUAA") for i in genes}
        self.proteasomes = {'Proteasomes': mol.Proteasome('Proteasomes', 'Proteasomes', 10)}
        self.metabolites = {'ATP': mol.Metabolite(0, 'ATP', 6000.0), 'AA': mol.Metabolite(1, 'AA', 4000.0), 'NT': mol.Metabolite(2, 'NT', 2000.0)}#anpassen an
        self.Helicase = {'Helicase_{0}'.format(i): rep.Helicase(i, 'Helicase_{0}'.format(i)) for i in xrange(0,2)}
        self.PolymeraseIII = {'PolymeraseIII_{0}'.format(i):rep.PolymeraseIII(i,'PolymeraseIII_{0}'.format(i)) for i in xrange(0,4)}
        self.DNA = {'DNA':rep.DNA('DNA','DNA', DNA_length, 2*DNA_length)}
        self.states.update(self.Helicase)
        self.states.update(self.PolymeraseIII)
        self.states.update(self.DNA)
        self.states.update(self.ribosomes)
        self.states.update(self.mrnas)
        self.states.update(self.metabolites)
        self.states.update(self.proteasomes)

        

        # initiate processes
        translation = proc.Translation(1, "Translation")
        translation.set_states(self.mrnas.keys(), self.ribosomes.keys())

        degradation = proc.Degradation(2, "Degradation")
        degradation.set_states([], self.proteasomes.keys() )

        replication = rep.Replication(1, "Replication", ATP_mol, NT_mol)
        replication.set_states(self.DNA.keys(), self.PolymeraseIII.keys() + self.Helicase.keys())
        #replication.set_states(self.mrnas.keys() + self.metabolites.keys(), self.ribosomes.keys() )
        self.processes = {"Translation":translation,
                          "Replication":replication,
                          "Degradation":degradation}

        self.logger=loggy.Logger()  # create the logger object

    def step(self):
        """
        Do one update step for each process.

        """
        keys = self.processes.keys()
        random.shuffle(keys)
        for p in keys:
            self.processes[p].update(self)
            protein = []
            g = 0
            for x in self.states.keys():
                if "Protein_" in x:
                    protein.append(x)
                    g += len(self.states[x])
            self.processes["Degradation"].set_states(protein, self.proteasomes.keys() )
            self.processes["Degradation"].update(self)
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
                self.logger.add_step(self.states.items()) # store the states of a timestep to the Logger object 

    def output(self): # wrapper: create the output data type after a simulation was done.  
        return self.logger.output() 

if __name__ == "__main__":
    c = Model()
    c.simulate(200, log=True)
    #c.output() # print the output data type of the Logger. Can be used for Plotting!!! 
    vis.mighty_plot(c.output(), 'time_course', ['Protein', 'Ribosomes', 'DNA'])
