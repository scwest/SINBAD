class Output():
    def __init__(self, output_filename):
        self._graph_filename = output_filename
        
    def export(self, graph):
        if len(graph) == 0:
            sys.stdout.write('No graphs to export\n')
            return
        sys.stdout.write('Exporting MGGs ... ')
        with open(self._graph_filename, 'w') as outfile:
            outfile.write('Significant splice variant\tDomain\tDomain\t'+\
                          'Splice variant2\tDomain type (all isoforms)\t'+\
                          'Domain type (high expr isoforms)\n')
            for edge in graph:
                outfile.write('\t'.join(edge) + '\n')
        sys.stdout.write('done\n')
        return