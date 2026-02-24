import create_graph as cg
from graphviz import Digraph






class Folgerungsgraph:
  activites = []
  variants = {}
  graph = Digraph()

  def __init__(self, act = [], var = {}):
    self.activites = act
    self.variants = var
  

  def drawFolgerungsgraph(self, format_type = 'svg'):
    graph = cg.createGraph(self.activites, self.variants)
    graph.render('testgraph', format = format_type, cleanup = 'True')