import sys 
import itertools

class Graphs():
    def __init__(self, references, min_threshold):
        self.ref = references
        self.min_threshold = min_threshold
    
    def construct(self):
        sys.stdout.write('Constructing MGGs\n')
        graph = []
        
        num_gene2gene = 0
        num_gene_with_sig = 0
        num_interactions = 0
        num_interactions_with_dom = 0
        
        l = str(len(self.ref.gene2gene))
        c = 1
        # only allow gene-genes that are already PPI (handled in References())
        for gene1, gene2s in self.ref.gene2gene.items(): 
            num_gene2gene += 1
            sys.stdout.write('\r\t'+str(c)+' of '+l)
            sys.stdout.flush()
            c += 1
            
            # ignore genes without any significant splice variants
            for svar in self.ref.gene2svars[gene1]:
                if svar in self.ref.significant_svars:
                    print(svar)
            
            if not sum([(svar in self.ref.significant_svars) for svar in self.ref.gene2svars[gene1]]): continue
            # command could be faster by continuing at first False instance
            num_gene_with_sig += 1
            
            domain_types_raw = self._get_domain_types(gene1, False)
            domain_types_filt = self._get_domain_types(gene1, True)
            
            for gene2 in gene2s:
                for svar1, svar2 in itertools.product(self.ref.gene2svars[gene1], self.ref.gene2svars[gene2]):
                    num_interactions += 1
                    
                    # ignore splice variants without known protein products
                    if svar1 not in self.ref.svar2protein:
                        continue
                    
                    # ignore splice variants that are insignificant
                    if svar1 not in self.ref.significant_svars:
                        continue
            
                    for domain1, domain2 in self._get_domain_pairs(gene1, svar2):
                        # ignore domains that are not 'gained' or 'ghost'
                        #    i.e. domains without unique attributes for survival significance
                        if domain_types_raw[domain1] == 'neither' and domain_types_filt[domain1] == 'neither':
                            continue
                        num_interactions_with_dom += 1
                        
                        edge = [svar1, domain1, domain2, svar2, domain_types_raw[domain1], domain_types_filt[domain1]]
                        graph.append(edge)
        sys.stdout.write('\n\tdone\n')
        sys.stdout.write('\tnumber of PPIs: '+str(num_gene2gene) + '\n')
        sys.stdout.write('\t   with significant splice variant: '+str(num_gene_with_sig) +'\n')
        sys.stdout.write('\tnumber of splice variant interactions: '+str(num_interactions) + '\n')
        sys.stdout.write('\t   with gained/ghost domains: '+str(num_interactions_with_dom) + '\n')
        sys.stdout.write('\tMGGs found: '+str(len(graph))+'\n')            
        return graph
    
    def _get_domain_pairs(self, gene, svar2):
        domain_pairs = []
        for svar1 in self.ref.gene2svars[gene]:
            for domain1, domain2 in itertools.product(self.ref.svar2domains[svar1], self.ref.svar2domains[svar2]):
                if domain2 in self.ref.domain2domain[domain1]:
                    domain_pairs.append((domain1, domain2))
        return domain_pairs
    
    def _get_domain_types(self, gene, filter_by_expression):
        domain_types = {}
        
        # identify the domains that belong to significant and non-significant splice variants
        sig, insig = set(), set()
        for svar in self.ref.gene2svars[gene]:
            if filter_by_expression:
                if not self._has_enough_expression(svar):
                    continue
            if svar in self.ref.significant_svars:
                sig |= self.ref.svar2domains[svar]
            else:
                insig |= self.ref.svar2domains[svar]
        
        # identify domain types and save
        for dom in sig - insig:
            domtypes[dom] = 'gained'
        for dom in insig - sig:
            domtypes[dom] = 'ghost'
        for dom in sig.intersection(insig):
            domtypes[dom] = 'neither'
        return domain_types
    
    def _has_enough_expression(self, svar):
        if self.proportion_expressed[svar] < 1-self.min_threshold:
            return False
        return True
    
    
    