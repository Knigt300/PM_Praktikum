import csv



def _parse_CSV_to_dict(input_file: str):
  ''' Parst csv-Datei in einen Eventlog, sortiert nach den Fällen.
  
  Parameter
  ---------
  log: str
    Datei, welche eingelesen werden soll.

  Returns
  -------
  dict
    Ein dict, wo die Schlüssel die Fall IDs aus der csv-Datei sind.
  '''
  eventlog = {}
  f = open(input_file, newline='', encoding='utf-8')
  reader = csv.DictReader(f)

  # Daten nach case_id sortiert einlesen, sind automatisch nach event_id intern sortiert
  for row in reader:
    if row['case_id'] in eventlog:
      eventlog[row['case_id']].append(row)
    else:
      eventlog[row['case_id']] = [row]

  f.close()
  return eventlog


def _filter_activities(log: dict, filtered_activites: list):
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


def _filter_variants(variants: dict, threshhold: int):
  ''' Löscht alle Varianten, welche unter der threshhold liegen.
  
  Funktion erstellt eine Kopie, bearbeitet diese udn gibt die bearbeitet Kopie zurück.

  Parameter
  ---------
  variants: dict
    Varianten mit Anzahl, welche gfiltert werden sollen.

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
  dict
    Dict, mit den Pfaden als Schlüssel und die Werte sind die Vorkommen des Pfades.
  '''
  variants = {}
  for case in log.keys():
    path = ''   # Pfad zu case
    for event in log[case]:
      path += ' ' + event['activity']
    # vorkommen von Pfad erhöhen
    if path in variants:
      variants[path] += 1
    else:   # erstes Vorkommen des Pfades => Pfad eintragen
      variants[path] = 1

  return variants


  