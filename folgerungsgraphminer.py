import create_graph as cg
from graphviz import Digraph


def filter_activities(log: dict, filtered_activites: list):
  ''' Löscht Aktivitäten bestimmt aus allen Fällen.

  Funktion arbeitet nicht mutierend und erstellt ein neues Log, welches bearbeitet wird.

  Parameter
  ---------
  log: dict
    Ereignisprotokoll, aus denen die Fälle gelöscht werden sollen.

  filtered_activities: list
    Eine Liste mit den Aktivitäten, welche gefiltert werden sollen.
  
  Returns
  -------
  dict
    Ein neuer, gefilterter Log.
  '''
  new_log = log.copy()
  for case in new_log.keys(): #case = liste, new_log = dict
    for event in new_log[case]: # event = dict
      if event['activity'] in filtered_activites:
        new_log[case].remove(event)
  
  return new_log


def filter_variants(variants: dict, threshhold: int):
  ''' Löscht alle Varianten, welche unter der threshhold liegen.
  
  Funktion erstellt eine Kopie, bearbeitet diese udn gibt die bearbeitet Kopie zurück.

  Parameter
  ---------
  variants: dict
    Varianten mit Anzahl, welche gefiltert werden sollen.

  threshhold: int
    Mindestanzahl an Vorkommen für gültig Aktivitäten.

  Returns
  -------
  dict
    Eine gefiltertes Varianten-dict.
  '''
  new_variants = variants.copy()
  to_delete = []

  for path in new_variants.keys():
    if new_variants[path] < threshhold:
      to_delete.append(path)

# Wir können nicht über das dict iterieren und Elemente löschen, also merken und später löschen
  for path in to_delete:
    del new_variants[path]
  
  return new_variants


def _get_variants(log: dict):
  '''Zählt die Pfade und deren Vorkommen in einem Log.

  Parameter
  ---------
  log: dict
    Ein Ereignissprotokoll, aus welchem die Pfade kommen.

  Returns:
    Dict, mit den Pfaden als Schlüssel und die Werte sind die Vorkommen des Pfades.
  '''
  variants = {}
  for case in log.keys():
    path = ''   # Pfad zu case
    for event in log[case]:
      # Leerzeichen wichtig, damit wir Aktivitäten aus dem Pfad erkennen können
      path += ' ' + event['activity']
    # vorkommen von Pfad erhöhen
    if path in variants:
      variants[path] += 1
    else:   # erstes Vorkommen des Pfades => Pfad eintragen
      variants[path] = 1

  return variants


def _get_activities(log:dict):
  '''Holt alle Aktivitäten aus einem Log
  
  Parameter
  ---------
    Ereignislog, aus dem die Aktivitäten gesucht werden

  Returns
  -------
    Eine Liste mit allen Aktivitäten, jede Aktivität kommt einmal vor
  '''

  activites = []

  for case in log.keys():
    for event in log[case]:
      if event['activity'] not in activites:
        activites.append(event['activity'])

  return activites


class Folgerungsgraph:
  activites = []
  variants = {}
  graph = Digraph()

  def __init__(self, log):
    self.activites = _get_activities(log)
    self.variants = _get_variants(log)
  

  def drawFolgerungsgraph(self, format_type = 'svg'):
    graph = cg.createGraph(self.activites, self.variants)
    graph.render('testgraph', format = format_type, cleanup = 'True')