import random
import molecules as molecules
import numpy.random as npr


class Process(object):
    """
    Parent for all cellular processes.
    """
    def __init__(self, id, name):
        self.id = id
        self.name = name
        #self.metabolites = metabolites


        self.enzyme_ids = []
        self.substrate_ids = []
        #self.metabolite_ids = []
        #self.metabolite = molecules.Metabolite()

    def set_states(self, substrate_ids, enzyme_ids):
        self.enzyme_ids = enzyme_ids
        #self.enzyme_ids = [1,2,3,4,5]
        self.substrate_ids = substrate_ids
        #self.substrate_ids = [5,4,3,5,6]
        #self.metabolite_ids = metabolite_ids

    def update(self, model):
        """
        Has to be implemented by child class.
        """
        pass


class Translation(Process):
    """
    Translation is instantiated in the Cell to produce proteins.

    Defines Translation process. It iterates over all ribosomes and decides what
    they should do. They either bind to mRNA or elongate/terminate a protein if
    they are already bound.

    """
    code = dict([('UCA', 'S'), ('UCG', 'S'), ('UCC', 'S'), ('UCU', 'S'),
                 ('UUU', 'F'), ('UUC', 'F'), ('UUA', 'L'), ('UUG', 'L'),
                 ('UAU', 'Y'), ('UAC', 'Y'), ('UAA', '*'), ('UAG', '*'),
                 ('UGU', 'C'), ('UGC', 'C'), ('UGA', '*'), ('UGG', 'W'),
                 ('CUA', 'L'), ('CUG', 'L'), ('CUC', 'L'), ('CUU', 'L'),
                 ('CCA', 'P'), ('CCG', 'P'), ('CCC', 'P'), ('CCU', 'P'),
                 ('CAU', 'H'), ('CAC', 'H'), ('CAA', 'Q'), ('CAG', 'Q'),
                 ('CGA', 'R'), ('CGG', 'R'), ('CGC', 'R'), ('CGU', 'R'),
                 ('AUU', 'I'), ('AUC', 'I'), ('AUA', 'I'), ('AUG', 'M'),
                 ('ACA', 'T'), ('ACG', 'T'), ('ACC', 'T'), ('ACU', 'T'),
                 ('AAU', 'N'), ('AAC', 'N'), ('AAA', 'K'), ('AAG', 'K'),
                 ('AGU', 'S'), ('AGC', 'S'), ('AGA', 'R'), ('AGG', 'R'),
                 ('GUA', 'V'), ('GUG', 'V'), ('GUC', 'V'), ('GUU', 'V'),
                 ('GCA', 'A'), ('GCG', 'A'), ('GCC', 'A'), ('GCU', 'A'),
                 ('GAU', 'D'), ('GAC', 'D'), ('GAA', 'E'), ('GAG', 'E'),
                 ('GGA', 'G'), ('GGG', 'G'), ('GGC', 'G'), ('GGU', 'G')])

    def __init__(self, id, name):
        super(Translation, self).__init__(id, name)

        # declare attributes
        self.__ribosomes = []
        self.__atp = []
        #self.__atp = self.atp
        #print(self.__atp)

    def update(self, model):
        """
        Update all mrnas and translate proteins.
        """
        self.__ribosomes = model.states[self.enzyme_ids[0]]
        #if model.states == {}:
        self.__atp = model.states["ATP"]
        self.__mrna = [x for x in self.substrate_ids if "MRNA" in x]
        for mrna_id in self.__mrna:
            #for atp_id in self.metabolite_ids:
                prot = None
                mrna = model.states[mrna_id]
                #atp = model.states[atp_id]

                if not mrna.binding[0]: #and self.__atp > 0:
                    self.initiate(mrna)
                else:
                    prot = self.elongate(mrna)
                if isinstance(prot, molecules.Protein):
                    if prot.id in model.states:
                        model.states[prot.id].append(prot)
                    else:
                        model.states[prot.id] = [prot]

    def initiate(self, mrna):
        """
        Try to bind to a given MRNA. Binding probability corresponds to the ribosome count.

        @type mrna: MRNA
        """
        if not mrna.binding[0]:  #  no mrna bound yet and target mrna still free at pos 0
            # bind a nascent protein to the 0 codon
            if npr.poisson(self.__ribosomes.count) > 1 and self.__atp > 0: # at least one binding event happens in time step
                # if a ribosome binds the position a new Protein is created and stored on the
                # position as if it were bound to the ribosome
               
                self.__atp.atpcount()
                
                print('\n new protein: {}'.format(self.__atp.count))
                mrna.binding[0] =  molecules.Protein("Protein_{0}".format(mrna.id),
                                                     "Protein_{0}".format(mrna.id),
                                                     self.code[mrna[0:3]])
                self.__ribosomes.count -= 1
            #if self.__atp <= 0:
                #break
                


    def elongate(self, mrna):
        """
        Elongate the new protein by the correct amino acid. Check if an
        MRNA is bound and if ribosome can move to next codon.
        Terminate if the ribosome reaches a STOP codon.

        @type return: Protein or False
        """

        # TODO: this needs to update in a random order
        for i, ribosome in enumerate(mrna.binding):
            if self.__atp <= 0:
                break
            if isinstance(ribosome, molecules.Protein):

                codon = mrna[i*3:i*3+3]
                aa = self.code[codon]
                #print('\r'.format(self.__atp))
                self.__atp.atpcount()
                #self.__atp = self.metabolite.atpcount()
                  
                #print('\r'.format(self.__atp)) 

                if aa == "*":  # terminate at stop codon
                    return self.terminate(mrna, i)

                if not mrna.binding[i + 1]:  # if the next rna position is free
                    mrna.binding[i] + aa
                    mrna.binding[i + 1] = mrna.binding[i]
                    mrna.binding[i] = 0
        return 0

    def terminate(self, mrna, i):
        """
        Splits the ribosome/MRNA complex and returns a protein.

        @type mrna: MRNA
        """

        protein = mrna.binding[i]  # bound mRNA
        mrna.binding[i] = 0
        self.__ribosomes.count += 1
        #self.__atp.atpcount()
        #self.__atp = self.metabolite.atpcount()
        
        #print(self.__atp)
        return protein


class Transcription(Process):
    """
    Implements mRNA transcription from genes on the chromosome.
    """

    def __init__(self, id, name):
        super(Transcription, self).__init__(id, name)

    # TODO: implement transcription