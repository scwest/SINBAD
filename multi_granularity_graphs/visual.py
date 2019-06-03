from graphviz import Digraph
import subprocess
import collections

from multi_granularity_graphs import Internal_network

class Visual():    
    def generate(self, edges, filename):
        inet = Internal_network()
        for edge in edges:
            inet.import_path(edge)
        inet.merge_nodes()
                
        f = Digraph('MGG', strict=True, format='svg')
        f = self._add_network(f, inet)
        
        f.render(filename=filename)
        subprocess.call(['rm', filename])
        return
    
    def _add_network(self, f, inet):
        for name in inet.depth_nodes[0]:
            node = inet.depth_nodes[0][name]
            f.node(node.number, label=node.name, \
                   shape='box', color='black', style='rounded,filled', fillcolor='#d4c9fc')
            for child in node.children:
                if child in inet.depth_nodes[1]:
                    color1 = 'white' 
                    if inet.depth_nodes[1][child].gg_raw == 'gained':
                        color1 = '#58d863'
                    if inet.depth_nodes[1][child].gg_raw == 'ghost':
                        color1 = '#91dfff'
                    color2 = 'white'
                    if inet.depth_nodes[1][child].gg_fil == 'gained':
                        color2 = '#58d863'
                    if inet.depth_nodes[1][child].gg_fil == 'ghost':
                        color2 = '#91dfff'
                    f.node(inet.depth_nodes[1][child].number, label=inet.depth_nodes[1][child].name, \
                           shape='box', color='black', style='striped', fillcolor=color1+':'+color2)
                    f.edge(node.number, inet.depth_nodes[1][child].number)
                    
        for name in inet.depth_nodes[1]:
            node = inet.depth_nodes[1][name]
            for child in node.children:
                if child in inet.depth_nodes[2]:
                    f.node(inet.depth_nodes[2][child].number, label=inet.depth_nodes[2][child].name,\
                           shape='box', color='black', style='filled', fillcolor='lightgray')
                    f.edge(node.number, inet.depth_nodes[2][child].number)
                    
        for name in inet.depth_nodes[2]:
            node = inet.depth_nodes[2][name]
            for child in node.children:
                if child in inet.depth_nodes[3]:
                    f.node(inet.depth_nodes[3][child].number, label=inet.depth_nodes[3][child].name,\
                           shape='box', color='black', style='rounded,filled', fillcolor='#afcbd6')
                    f.edge(node.number, inet.depth_nodes[3][child].number)
        
        return f
    
    def _set_node_attributes(self, f, node_nums, edge):
        '''
        degraded
        will delete when all other code has been tested for next release
        '''
        f.node(node_nums[0], shape='ellipse', color='black', style='filled', fillcolor='#d4c9fc')
        if edge[4] == 'ghost':
            f.node(node_nums[1], shape='box', color='black', style='filled', fillcolor='white')
        else:
            f.node(node_nums[1], shape='box', color='black', style='filled', fillcolor='#58d863')
        f.node(node_nums[2], shape='box', color='black', style='filled', fillcolor='lightgray')
        f.node(node_nums[3], shape='ellipse', color='black', style='filled', fillcolor='#afcbd6')
        return f