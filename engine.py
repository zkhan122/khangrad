from graphviz import Digraph
from IPython.display import display



class Value:
    def __init__(self, data, _children=(), _op=''):
        self.data = data
        self._prev = set(_children) # tup -> set for efficiency purposes
        self._op = _op

    def __repr__(self):
        return f"Value(data={self.data})"

    def __add__(self, other):
        out = Value(self.data + other.data, (self, other,), '+')
        return out

    def __mult__(self, other):
        out = Value(self.data * other.data, (self, other), '*')
        return out


def trace(root):
    nodes, edges = set(), set()
    def build(v: Value):
        if v not in nodes:
            nodes.add(v)
            for child in v._prev:
                edges.add((child, v))
                build(child)
    build(root)
    return nodes, edges

def draw_dot(root):
    dot = Digraph(format='svg', graph_attr={'rankdir': 'LR'})

    nodes, edges = trace(root)
    for n in nodes:
        uid = str(id(n))

        # for any vlsue in the graph, create a rectangular 'record' node for it
        dot.node(name = uid, label = "{data %.4f}" % (n.data, ), shape='record')
        if n._op:
            # if this value is a result of some operation, create an op node for it
            dot.node(name=uid + n._op, label = n._op)
            # and connect the node to it
            dot.edge(uid + n._op, uid)

    for n1, n2 in edges:
        dot.edge(str(id(n1)), str(id(n2)) + n2._op)

    return dot


if __name__ == "__main__":
    a = Value(2.0)
    b = Value(-3.0)
    c = Value(10.0)
    print(a)
    print(b)

    print(a.__add__(b))
    print(a.__mult__(b))
    print(a.__mult__(b).__add__(c)) # a*b+c

    d = a.__mult__(b).__add__(c) #  -6 from a*b and 10 from c

    print(d._prev)

    op_graph = draw_dot(d)
    display(op_graph)