class DependencySolver(object):
    def __init__(self, get_dependencies):
        '''
        get_dependencies -- a callable that given a node, returns a list of other nodes that node depends on
        As nodes are inserted with the add_node() method, the order in which the nodes can be visited (from 0 to n)
        such that dependent nodes are visited first, will be saved to the node_order list
        '''
        self.node_order = []
        self._unresolved_nodes = {}
        self._get_dependencies = get_dependencies

    def add_node(self, node):
        self._add_node(node)
        self._compute_ordering()

    def _add_node(self, node):
        if node in self._unresolved_nodes or node in self.node_order:
            return
        dependencies = set([x for x in self._get_dependencies(node) if x not in self.node_order])

        self._unresolved_nodes[node] = dependencies
        for dependency in dependencies:
            self._add_node(dependency)

    def _compute_ordering(self):
        while self._unresolved_nodes:
            nodes_without_deps = [k for k, v in self._unresolved_nodes.iteritems() if not v]
            if not nodes_without_deps:
                raise RuntimeError('Cyclical dependies exist for nodes: %s' % self._unresolved_nodes.keys())
            self.node_order.extend(nodes_without_deps)
            self._unresolved_nodes = dict([
                (k, v) for k, v in self._unresolved_nodes.iteritems() if v
                ])

            for dependencies in self._unresolved_nodes.itervalues():
                dependencies -= set(nodes_without_deps)

if __name__ == '__main__':
    def dependency_func(x):
        return {
            1: [2,3,4],
            2: [],
            3: [],
            4: [5],
            5: [],
            6: [7],
            7: [4,5,8],
            8: [],
            }[x]
    
    dep_solver = DependencySolver(dependency_func)
    dep_solver.add_node(6)
    dep_solver.add_node(1)
    print dep_solver.node_order
