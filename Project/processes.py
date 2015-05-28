import random
import molecules
import numpy.random as npr
from Input.KnowledgeBase import KnowledgeBase as know


class Process(object):
    """
    Parent for all cellular processes.
    """
    def __init__(self, id, name):
        self.id = id
        self.name = name


        self.enzyme_ids = []
        self.substrate_ids = []

    def set_states(self, substrate_ids, enzyme_ids):
        self.enzyme_ids = enzyme_ids
        self.substrate_ids = substrate_ids

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
        self.kb = know()
        # declare attributes
        self.__ribosomes = []
        self.__atp = []
        self.__aa = []

    def update(self, model):
        """
        Update all mrnas and translate proteins and current metabolites.
        """
        self.__ribosomes = model.states[self.enzyme_ids[0]]
        self.__atp = model.states['ATP']
        self.__mrna = [x for x in self.substrate_ids if "MRNA" in x]
        self.__aa = model.states['AA']
        for mrna_id in self.__mrna:
            prot = None
            mrna = model.states[mrna_id]

            if not mrna.binding[0]:
                self.initiate(mrna)
            else:
                prot = self.elongate(mrna)
            if isinstance(prot, molecules.Protein):
                if prot.id in model.states:
                    model.states[prot.id].append(prot)
                else:
                    model.states[prot.id] = [prot]

        print self.__ribosomes

    def initiate(self, mrna):
        """
        Try to bind to a given MRNA. Binding probability corresponds to the ribosome count.

        @type mrna: MRNA
        """
        if not mrna.binding[0]:  #  no mrna bound yet and target mrna still free at pos 0
            # bind a nascent protein to the 0 codon
            if npr.poisson(self.__ribosomes.count) > 1 and self.__atp.count > 0: # at least one binding event happens in time step
                # if a ribosome binds the position a new Protein is created and stored on the
                # position as if it were bound to the ribosome
                # ATP has to be available
                halflife = self.kb.get_protein_hl(mrna.id)
                halflife = halflife.replace(',', '.')
                halflife = float(halflife)
                self.__atp.metacount(1)
                
                mrna.binding[0] =  molecules.Protein("Protein_{0}".format(mrna.id),
                                                     "Protein_{0}".format(mrna.id),
                                                     self.code[mrna[0:3]],
                                                     halflife = halflife)
                self.__ribosomes.count -= 1
                


    def elongate(self, mrna):
        """
        Elongate the new protein by the correct amino acid. Check if an
        MRNA is bound and if ribosome can move to next codon.
        Terminate if the ribosome reaches a STOP codon.

        @type return: Protein or False
        """

        # TODO: this needs to update in a random order
        for i, ribosome in enumerate(mrna.binding):
            if self.__atp.count <= 0 or self.__aa.count <= 0: #if there is no more ATP, elongation can't proceed
                break
            if isinstance(ribosome, molecules.Protein):

                codon = mrna[i*3:i*3+3]
                aa = self.code[codon]
                self.__atp.metacount(1)
                self.__aa.metacount(1)

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
        self.__atp.metacount(1)
       
        return protein



class Transcription(Process):
    """
    Implements mRNA transcription from genes on the chromosome.
    """

    def __init__(self, id, name):
        super(Transcription, self).__init__(id, name)

    # TODO: implement transcription

class Degradation(Process):
    """
    Implements Protein Degradation by chance
    """
    count_s = 0
    global count_s

    def __init__(self, id, name):
        super(Degradation, self).__init__(id, name)
        self.__proteasomes = []

    def set_states(self, substrate_ids, enzyme_ids):
        self.protein_ids = substrate_ids
        self.enzyme_ids = enzyme_ids

    
    def update(self, model):

        #Regenerates amount of Proteasomes for every step
        global count_s
        self.__proteasomes = model.states[self.enzyme_ids[0]]
        self.__proteasomes.count = 10
        count_s += 1
        print 'count_s', count_s

        #Checks if there are any proteins available, computes a value sigma (depending on halflife) which is compared
        # to random number between 0 and 1. If random number is < than sigma, protein is degradated and one proteasom is busy.
        # If no proteasom is left, sigma is half as big as befor (protein is more unlikely to be degradated)
        for p in self.protein_ids:
            if len(model.states[p]) != 0:
                hwz = model.states[p][0].halflife
                sig = float(1.0/(2.0*hwz*60))
                for pos in model.states[p]:
                    if self.__proteasomes.count != 0:
                        z = random.uniform(0,1)
                        print z
                        print sig
                        if z < sig:
                            print 'Protein killed'
                            self.__proteasomes.count -= 1
                            print 'Anzahl:', self.__proteasomes.count
                            del model.states[p][0]
                        else:
                            print 'Nothing happens'
                    else:
                        z = random.uniform(0,1)
                        sig = float(1.0/(4.0*hwz*60))
                        print z
                        print sig
                        if z < sig:
                            print 'Protein killed without Proteasome'
                            del model.states[p][0]
                        else:
                            print 'Nothing happens without Proteasome'