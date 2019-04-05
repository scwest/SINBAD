class Outputs():
    def __init__(self, output_filename):
        self._graph_filename = output_filename
        
    def export(self, graph):
        with open(self._graph_filename, 'w') as outfile:
            for edge in graph:
                outfile.write('\t'.join(edge) + '\n')
        return