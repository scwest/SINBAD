from multi_granularity_graphs import Inputs
from multi_granularity_graphs import References
from multi_granularity_graphs import Graphs

class Control():
    def main(self):
        inputs = Inputs()
        
        references = References()
        references.set_all_references(inputs.args)
        
        graphs = Graphs(references, inputs.args['min_threshold'])
        graphs.construct()
        
        output = Output(inputs.args['output'])
        output.export(graphs)
        
        return
    
def smain():
    stick = Control()
    stick.main()
    return
