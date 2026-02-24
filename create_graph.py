import graphviz as g


def _get_occurences_node_from_edges(edges:dict):
  occ_nodes = {}

  for (a,b) in edges.keys():
    # start ist nie b, daher Extrafall
    if a == 'start':
      if a in occ_nodes.keys():
        occ_nodes[a] += edges[(a,b)]
      else:
        occ_nodes[a] = edges[(a,b)]
    # kein Extrafall für End, da es normal benutzt wird
    if b in occ_nodes.keys():
      occ_nodes[b] += edges[(a,b)]
    else:
      occ_nodes[b] = edges[(a,b)]

  return occ_nodes


def createGraph(nodes:list, variants:list, type = 'svg'):
  '''Erstellt einen Graphen anhand der gegebenen Knoten und Varianten 

  Parameter
  ---------
  nodes: list
    Eine Liste mit allen Knoten

  variants: dict
    Ein Dict, wo die Schlüssel die Pfade sind und der Werte deren Vorkommen

  type: string
    Ein String, der den Dateityp der Ausgab bestimmt. Im Normalfall wird eine svg gemacht.

  Returns
  -------
  Digraph
    Ein Digraph aus der graphviz Bibliothek
  '''
  dot = g.Digraph()


  

  edges = {}

  for v in variants.keys():
    # Man kann im Digraph nicht sehen, welche Kanten wir haben,
    # also Kanten erst zusammenzählen und dann eintragen
    
    # Pfad aus Schlüssel bauen, an den Leerzeichen aufteilen
    path = v.split()
    # Start und Ende des Pfades erstellen
    if ('start', path[0]) in edges.keys():
      edges[('start', path[0])] += variants[v]
    else:
      edges[('start', path[0])] = variants[v]
    
    if (path[-1], 'end') in edges.keys():
      edges[(path[-1], 'end')] += variants[v]
    else:
      edges[(path[-1], 'end')] = variants[v]
  
    # Restliche Kanten des Pfades eintragen
    for i in range(len(path)-1):
      if (path[i],path[i+1]) in edges.keys():
        edges[(path[i],path[i+1])] += variants[v]
      else:
        edges[(path[i],path[i+1])] = variants[v]
      
  # Kanten im graphen einschreiben
  for (a,b) in edges.keys():
    dot.edge(a, b, label=str(edges[(a,b)]), fillcolor='#006699', color = '#006699', fontcolor = '#000000')


  occ_nodes = _get_occurences_node_from_edges(edges)

  # Start und Ende mit Dreieck und Viereck erstellen
  dot.node('start', '\u25B6' + '\n' + str(occ_nodes['start']), shape = 'box', style = 'filled', fillcolor='#000000', color = '#FFFFFF', fontcolor = '#FFFFFF')
  dot.node('end', '\u25FC' + '\n' + str(occ_nodes['start']), shape = 'box', style = 'filled', fillcolor='#000000', color = '#FFFFFF', fontcolor = '#FFFFFF')
  
  # Knoten einfügen
  for n in nodes:
    dot.node(str(n), label=str(n) + '\n' + str(occ_nodes[n]), shape = 'box', style = 'filled', fillcolor='#000000', color = '#FFFFFF', fontcolor = '#FFFFFF')

  return dot


'''
label=<str(n)<BR />
        edges[n]>

'''