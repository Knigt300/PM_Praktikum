import graphviz as g

def renderGraph(nodes:list, paths:list):
  '''Erstellt einen Graphen anhand der gegebenen Knoten/Kanten

  Kanten werden hier als Pfade gegeben. Ergebniss wird als testgraph.svg gespeichert.

  Parameter
  ---------
  nodes: list
    Eine Liste mit allen Knoten

  paths:list
    Eine Liste mit allen Pfaden, welche selber als Liste von strings dargestellt werden
  '''
  dot = g.Digraph()

  dot.node('start', '\u25B6', shape = 'box', style = 'filled', fillcolor='#000000', color = '#FFFFFF', fontcolor = '#FFFFFF')
  dot.node('end', '\u25FC', shape = 'box', style = 'filled', fillcolor='#000000', color = '#FFFFFF', fontcolor = '#FFFFFF')

  for n in nodes:
    dot.node(str(n), label=f'{n}', shape = 'box', style = 'filled', fillcolor='#000000', color = '#FFFFFF', fontcolor = '#FFFFFF')

  for path in paths:
    dot.edge('start', path[0], color = '#000000')
    dot.edge(path[-1], 'end', color = '#000000')
    for i in range(len(path)-1):
      dot.edge(path[i],path[i+1], color = '#000000')

  dot.render('testgraph', format = 'svg', cleanup = 'True')