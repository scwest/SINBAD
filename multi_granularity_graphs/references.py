from collections import defaultdict
import numpy as np
import sys 

class References():
    def __init__(self):
        self.gene2gene = defaultdict(set)
        self.gene2svars = defaultdict(set)
        self.svar2protein = {}
        self.domain2domain = defaultdict(set)
        self.svar2domains = defaultdict(set)
        self.significant_svars = set()
        self.proportion_expressed = {}
        
    def set_all_references(self, locations):
        sys.stdout.write('Uploading input ... ')
        sys.stdout.flush()
        self.set_domain2domain(locations['domain2domain'])
        self.set_gene2svars(locations['gene2svars'])
        self.set_svar2protein(locations['svar2protein'])
        self.set_gene2gene(locations['gene2gene'])
        self.set_svar2domains(locations['svar2domains'])
        self.set_significant_svars(locations['significant_svars'])
        self.set_proportion_expressed(locations['expression'])
        sys.stdout.write('done\n')
        return
        
    def set_domain2domain(self, filename):
        with open(filename, 'r') as infile:
            for line in infile:
                line = line.strip().split('\t')
                self.domain2domain[line[0]].add(line[1])
                self.domain2domain[line[1]].add(line[0])
        return
        
    def set_gene2gene(self, filename): # after set_ensg2ensts and set_enst2ensp
        with open(filename, 'r') as infile:
            for line in infile:
                line = line.strip().split('\t')
                self.gene2gene[line[0]].add(line[1])
                self.gene2gene[line[1]].add(line[0])
        return
    
    def set_gene2svars(self, filename):
        with open(filename, 'r') as infile:
            c = 0
            for line in infile:
                c += 1
                try:
                    ensg, enst = line.strip().split('\t')
                    self.gene2svars[ensg].add(enst)
                except:
                    print('Warning: Issue with gene2svars file. See line number '+str(c)+':\n'+line)
        return
    
    def set_svar2protein(self, filename):
        with open(filename, 'r') as infile:
            for line in infile:
                enst, ensp = line.strip().split('\t')
                self.svar2protein[enst] = ensp
        return
    
    def set_svar2domains(self, filename):
        with open(filename, 'r') as infile:
            for line in infile:
                enst, domains = line.strip().split('\t')
                domains = set(domains.split(','))
                self.svar2domains[enst] = domains
        return   
    
    def set_significant_svars(self, filename):
        with open(filename, 'r') as infile:
            infile.readline()
            for line in infile:
                line = line.strip().split('\t')
                if float(line[3]) < 0.1:
                    self.significant_svars.add(line[0])
        return
    
    def set_proportion_expressed(self, filename):
        with open(filename, 'r') as infile:
            infile.readline()
            for line in infile:
                name, rest = line.strip().split(',', 1)
                tpms = rest.split(',')
                prop = float(np.count_nonzero([float(x) for x in tpms])) / len(tpms)
                self.proportion_expressed[name] = prop
        return