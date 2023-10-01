import graphviz

s = graphviz.Source.from_file("civgraph.txt")


d = graphviz.Digraph()
d.edges