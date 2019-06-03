import collections

class Internal_network():
    def __init__(self):
        self.depth_nodes = collections.defaultdict(dict) # [depth][name] = node
        self.next_num = 1
        
    class Node():
        def __init__(self):
            self.parents = []
            self.children = []
            self.number = []
            self.name = ''
            self.gg_raw = ''
            self.gg_fil = ''
            
    def import_path(self, edge):
        self.add_node(edge[0], 0)
        self.add_node(edge[1], 1)
        self.add_node(edge[2], 2)
        self.add_node(edge[3], 3)
        
        self.depth_nodes[1][edge[1]].gg_raw = edge[4]
        self.depth_nodes[1][edge[1]].gg_fil = edge[5]
        
        self.add_edge(edge[0], 0, edge[1], 1)
        self.add_edge(edge[1], 1, edge[2], 2)
        self.add_edge(edge[2], 2, edge[3], 3)
        return
    
    def add_node(self, name, depth):
        if name not in self.depth_nodes[depth]:
            self.depth_nodes[depth][name] = self.Node()
            self.depth_nodes[depth][name].name = name
            self.depth_nodes[depth][name].number = str(self.next_num)
            self.next_num += 1
        return
    
    def add_edge(self, name1, depth1, name2, depth2):
        self.depth_nodes[depth1][name1].children.append(self.depth_nodes[depth2][name2].name)
        self.depth_nodes[depth2][name2].parents.append(self.depth_nodes[depth1][name1].name)
        return
    
    def merge_nodes(self):
        groups_set = collections.defaultdict(set)
        groups_mem = collections.defaultdict(set)
        groups_cor = {}
        next_group = 1
        
        for name in self.depth_nodes[3]:
            node = self.depth_nodes[3][name]
            cor = node.name.split('-')[0]
            group_matches = set()
            for k, s in groups_set.items():
                if self.same_list(node.parents, s):
                    group_matches.add(k)
            if not group_matches:
                groups_set[next_group] = set(node.parents)
                groups_mem[next_group] = {node.name}
                groups_cor[next_group] = cor
                next_group += 1
            else:
                found_cor = False
                for match in group_matches:
                    if cor == groups_cor[match]:
                        groups_mem[match].add(node.name)
                        found_cor = True
                        break
                if not found_cor:
                    groups_set[next_group] = set(node.parents)
                    groups_mem[next_group] = {node.name}
                    groups_cor[next_group] = cor
                    next_group += 1
                    
        for group in groups_cor:
            if len(groups_mem[group]) <= 1:
                continue
            new_name = groups_cor[group] + '-'
            new_name += ','.join(sorted([self.depth_nodes[3][x].name.split('-')[1] for x in groups_mem[group]]))
            node = self.Node()
            node.parents = groups_set[group]
            node.name = new_name
            node.number = str(self.next_num)   
            self.next_num += 1         
            
            self.depth_nodes[3][new_name] = node
            for parent in node.parents:
                self.depth_nodes[2][parent].children.append(new_name)                    
            
            for mem in groups_mem[group]:
                del self.depth_nodes[3][mem]
        
        return
    
    def same_list(self, l, s):
        if set(l) == set(s):
            return True 
        return False
            
        