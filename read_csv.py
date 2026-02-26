import csv



def parse_CSV_to_dict(input_file: str):
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

  #Daten nach Startzeit sortieren
  for case in eventlog.keys():
    eventlog[case].sort(key= lambda x: x['start_timestamp'])
  return eventlog


