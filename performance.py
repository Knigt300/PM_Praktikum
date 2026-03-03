import datetime as dt

# log aus aufgabe 1 bearbeiten/erweitern
# einen case nehmen und dort die einzelnen Events neue Attribute geben

# TODO Wartezeit naive bestimmen (Aktivitäten sind zeitlich sortiert) oder sicher gehen?
# activitäten nach zeitlichen reihenfolge sortieren?

# Zeitlich gesehen passiert a.start b.start b.ende a.ende nicht
# a.start b.start a.ende b.ende kann passieren

def _get_activity_waittime(case:list):
  ''' Gibt jeder Aktivität die Wartezeit an
  
  Diese Funktion arbeiteet mutierend

  Parameter
  ---------
  case: list
    Eine Liste, welche nach den Startzeiten der Aktivitäten sortiert ist
  '''

  no_time = dt.timedelta(seconds= 0)  # Konstante um zu gucken ob eine Zeit ngeativ ist
  total_wait_time = dt.timedelta(seconds= 0)

  # -1, da letzte Aktivität keine nachfolgende Wartezeit hat
  for i in range(len(case) - 1):
    # Wartezeit bestimmen
    wait_time = dt.datetime.strptime(case[i+1]['start_timestamp'], '%Y-%m-%d %H:%M:%S') - dt.datetime.strptime(case[i]['end_timestamp'], '%Y-%m-%d %H:%M:%S')
      
    # prüfen, ob nächste Aktivität vor unserem Ende aufhört
    if wait_time > no_time:
      total_wait_time += wait_time
      case[i]['wait_time'] = wait_time
    else:
      case[i]['wait_time'] = no_time

  case[-1]['wait_time'] = no_time # letzter Aktivität auch das Attribut geben

  


def _calculate_case_durations(case:list):
  ''' Berechnet die Zeit eines Cases

  Ab dieser Funktion ist case ein dict und keine Liste mehr
  
  Parameters
  ----------
  case: list
    Ein Case in Form einer Liste

  Returns
  ------
    Ein dict, wo man auf die Metriken und Aktivitäten zugreifen kann
    'activities' für die Aktivitätenliste, 'duration' für die gesamte Dauer,
    'average_act_duration' für die Durchschnittliche dauer,
    'average_wait' für die durchschnittliche Wartezeit
  '''
  num_acitivties = len(case)
  average_duration = dt.timedelta(seconds= 0) # Datum soll Dauer zusammenrechnen, daher mit 0 initialisieren
  waiting_time = dt.timedelta(seconds=0)      

  start_time = dt.datetime.strptime(case[0]['start_timestamp'], '%Y-%m-%d %H:%M:%S')
  end_time = dt.datetime.strptime(case[0]['end_timestamp'], '%Y-%m-%d %H:%M:%S')

  for activity in case:
    start_activity = dt.datetime.strptime(activity['start_timestamp'], '%Y-%m-%d %H:%M:%S')
    end_activity = dt.datetime.strptime(activity['end_timestamp'], '%Y-%m-%d %H:%M:%S')
    average_duration += end_activity - start_activity
    
    
    if end_time < end_activity:
      end_time = end_activity

    waiting_time += activity['wait_time']
   
    activity['duration'] = end_activity - start_activity

  # case sind Listenelemente, dict zuweisung geht nicht
  new_case = {}

  new_case['average_wait'] = waiting_time / (num_acitivties -1) # letzte Aktivität hat keine Wartezeit, daher -1
  new_case['average_act_duration'] = average_duration / num_acitivties
  new_case['activities'] = case
  new_case['duration'] = end_time - start_time
  new_case['num_act'] = len(new_case['activities'])

  return new_case

# mutierend
def peformance_for_log(log:dict):
  # errechnet schon durchschnittliche warte/prozess Zeit, muss nicht für bottlneck wiederholt werden
  for case in log.keys():
    _get_activity_waittime(log[case])
    log[case] = _calculate_case_durations(log[case])
    

  average_dur_act = dt.timedelta(seconds=0)
  average_dur_wait = dt.timedelta(seconds=0)

  total_act = 0
  for case in log.keys():
    num_act = log[case]['num_act']
    total_act += num_act
    average_dur_wait += log[case]['average_wait'] * (num_act -1)
    average_dur_act += log[case]['average_act_duration'] * num_act

  log['average_dur_act'] = average_dur_act / total_act
  log['average_dur_wait'] = average_dur_wait / (total_act - len(log.keys())) # in jedem case gibt es ein -1, daher die -1 mitzählen


def get_bottlenecks(log:dict):
  # TODO genaue def von Bottleneck erfragen (pro Fall oder gesmamt angucken)
  act_wait_time = {}

  # totale Wartezeit für alle vorkommenden Aktivitätspaare berechnen
  for case in log.keys():
    if 'KSV' in case: # Schlüssle soll Fall und keine Metrik sein
      for i in range(len(log[case]['activities']) - 1):
        # wait time
        curr_act = log[case]['activities'][i]
        next_act = log[case]['activities'][i+1]
        path_wait = curr_act['activity'] + ' ' +  next_act['activity']

        # activity duration
        act_dur = dt.datetime.strptime(curr_act['end_timestamp'], '%Y-%m-%d %H:%M:%S') - dt.datetime.strptime(curr_act['start_timestamp'], '%Y-%m-%d %H:%M:%S')

        if path_wait in act_wait_time.keys():
          act_wait_time[path_wait] = (act_wait_time[path_wait][0] + curr_act['wait_time'],
                                      act_wait_time[path_wait][1] + 1)
        else:
          act_wait_time[path_wait] = (curr_act['wait_time'], 1)

        if curr_act['activity'] in act_wait_time.keys():
          act_wait_time[curr_act['activity']] = (act_wait_time[curr_act['activity']][0] + act_dur,
                                                 act_wait_time[curr_act['activity']][1] + 1 )
        else:
          act_wait_time[curr_act['activity']] = (act_dur, 1)

      # Aktivitätsdauer der letzten Aktivität nachholen
      curr_act = log[case]['activities'][-1]
      act_dur = (dt.datetime.strptime(curr_act['end_timestamp'], '%Y-%m-%d %H:%M:%S') - 
                dt.datetime.strptime(curr_act['start_timestamp'], '%Y-%m-%d %H:%M:%S'))
      if curr_act['activity'] in act_wait_time.keys():
        act_wait_time[curr_act['activity']] = (act_wait_time[curr_act['activity']][0] + act_dur,
                                               act_wait_time[curr_act['activity']][1] + 1 )
      else:
        act_wait_time[curr_act['activity']] = (act_dur, 1)

  # Durchschnittliche Wartezeit bestimmen
  # durchscnittliche Wartezeit pro Aktion bestimmen, danach
  # durchschnittliche Wartezeit über alle Aktionen bestimmen
  average_wait_times = {}
  average_act_time = {}
  total_wait = dt.timedelta(seconds= 0)
  num_act_pairs = 0
  num_act = 0
  total_act = dt.timedelta(seconds= 0)

  for path in act_wait_time.keys():
    # wenn Leerzeichen gefunden -> Wartezeit, da zwei Aktivitäten
    if ' ' in path:
      average_wait_times[path] = act_wait_time[path][0] / act_wait_time[path][1]
      total_wait += act_wait_time[path][0]
      num_act_pairs += act_wait_time[path][1]
    # Sonst Aktivitätsdauer
    else:
      average_act_time[path] = act_wait_time[path][0] / act_wait_time[path][1]
      total_act += act_wait_time[path][0]
      num_act += act_wait_time[path][1]
  
  total_average_wait = total_wait / num_act_pairs
  average_act_time = total_act / num_act
  
  bottlenecks = {}
  bottlenecks['problems'] = []
  bottlenecks['threshhold_wait'] = total_average_wait
  bottlenecks['threshhold_act'] = average_act_time
  for path in average_wait_times.keys():
    if average_wait_times[path] > total_average_wait and ' ' in path:
      bottlenecks['problems'].append((path,average_wait_times[path]))
    elif average_wait_times[path] > average_act_time and ' ' not in path:
      bottlenecks['problems'].append((path,average_wait_times[path]))

  return bottlenecks


def get_longest_cases(log:dict, num_cases = 1):
  ''' Sucht nach den längsten Fällen

  Parameter
  ---------
  log: dict
    Das Log aus welchem die Fälle kommen

  num_cases: int 
    Anzahl der Fälle, die ausgegeben werden sollen
  '''
  long_cases = []

  for case in log.keys():
    if 'KSV' in case: # alle Fälle haben KSV im Namen, einige Metriken sind auch Schlüssel, diese müssen wir ignorieren
      # Anfangs 'irgendwelche' logs nehmen
      if len(long_cases) < num_cases:
        long_cases.append(log[case])
      # logs vergleichen um längsten zu finden
      else:
        # ist einer der bisher längsten Fälle kürzer als der aktuelle?
        for i in range(len(long_cases)):
          if long_cases[i]['duration'] < log[case]['duration']:
            long_cases[i] = log[case]
            break # break, da wir nur einen Fall ersetzten wollen

  return long_cases

  