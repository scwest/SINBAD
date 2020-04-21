import sys 
import itertools

from multi_granularity_graphs import Visual

class Graphs():
    def __init__(self, references, min_threshold):
        self.ref = references
        self.min_threshold = min_threshold
        self.graphs = {} # self.graphs[gene] = Graph()
        
    class Graph():
        '''
        Each graph represents the Multi-Granularity Graph associated with a gene (possibly multiple splice variants).
        '''
        def __init__(self):
            self.edges = []
            self.visual = Visual()
            
        def add_edge(self, svar1, domain1, domain2, svar2, domain_type_raw, domain_type_filt):
            self.edges.append([svar1, domain1, domain2, svar2, domain_type_raw, domain_type_filt])
            return
        
        def visualize(self, output_filename):
            self.visual.generate(self.edges, output_filename)
            return
        
    class _Report():
        '''
        This class was added to simplify the self.construct() method.
        It conducts all the user level communication so that the self.construct() 
        method doesn't look cluttered.
        '''
        def __init__(self, total):
            self.num_gene2gene = 0
            self.num_gene_with_sig = 0
            self.num_interactions = 0
            self.num_interactions_with_dom = 0
            self.c = 1
            self.total = str(total)
            self.num_mggs = 0
            
        def initial_to_system(self):
            sys.stdout.write('Constructing MGGs\n')
            return
        
        def iteration(self):
            sys.stdout.write('\r\t'+str(self.c)+' of '+self.total)
            sys.stdout.flush()
            self.c += 1
            return
        
        def final_to_system(self):
            sys.stdout.write('\n\tdone\n')
            sys.stdout.write('\tnumber of PPIs: '+str(self.num_gene2gene) + '\n')
            sys.stdout.write('\t   with significant splice variant: '+str(self.num_gene_with_sig) +'\n')
            sys.stdout.write('\tnumber of splice variant interactions: '+str(self.num_interactions) + '\n')
            sys.stdout.write('\t   with gained/ghost domains: '+str(self.num_interactions_with_dom) + '\n')
            sys.stdout.write('\tTotal MGGs created: '+str(self.num_mggs)+'\n')
            #sys.stdout.write('\tMGG paths found: '+str(len(graph))+'\n') 
            return
    
    def construct(self):
        '''
        This full functionality of this class is utilized by calling this method. 
        self.construct() will generate all the graphs associated with the input data. 
        '''
        report = self._Report(len(self.ref.gene2gene))
        report.initial_to_system()
        
        # only allow gene-genes that are already PPI (handled in References())
        for gene1, gene2s in self.ref.gene2gene.items(): 
            report.iteration()
            report.num_gene2gene += 1
                        
            # ignore genes without any significant splice variants
            if not sum([(svar in self.ref.significant_svars) for svar in self.ref.gene2svars[gene1]]): 
                continue
            report.num_gene_with_sig += 1
                       
            domain_types_raw = self._get_domain_types(gene1, False)
            domain_types_filt = self._get_domain_types(gene1, True)
            
            for gene2 in gene2s:
                for svar1, svar2 in itertools.product(self.ref.gene2svars[gene1], self.ref.gene2svars[gene2]):
                    report.num_interactions += 1
                    
                    # ignore splice variants without known protein products
                    if self.ref.svar2protein:
                        if svar1 not in self.ref.svar2protein: 
                            continue
                    # ignore splice variants that are insignificant
                    if svar1 not in self.ref.significant_svars: 
                        continue
            
                    for domain1, domain2 in self._get_domain_pairs(gene1, svar2):
                        # ignore domains that are not 'gained' or 'ghost'
                        if domain_types_raw[domain1] == 'neither' and domain_types_filt[domain1] == 'neither':
                            continue
                        report.num_interactions_with_dom += 1
                        
                        if domain1 not in domain_types_filt:
                            domain_types_filt[domain1] = '-'
                        if domain1 not in domain_types_raw:
                            domain_types_raw[domain1] = '-'
                        
                        if gene1 not in self.graphs:
                            self.graphs[gene1] = self.Graph()
                            report.num_mggs += 1
                        self.graphs[gene1].add_edge(svar1, domain1, domain2, svar2, domain_types_raw[domain1], domain_types_filt[domain1])
                            
                        
        report.final_to_system()                        
        return
    
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
            domain_types[dom] = 'gained'
        for dom in insig - sig:
            domain_types[dom] = 'ghost'
        for dom in sig.intersection(insig):
            domain_types[dom] = 'neither'
        return domain_types
    
    def _has_enough_expression(self, svar):
        if svar in self.ref.proportion_expressed:
            if self.ref.proportion_expressed[svar] < 1-self.min_threshold:
                return False
        else:
            sys.stdout.write('\nWarning: '+svar+' is not in the expression file.\n')
            return False
        return True
    
    
    