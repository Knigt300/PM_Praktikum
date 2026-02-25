import datetime as dt

# log aus aufgabe 1 bearbeiten/erweitern
# einen case nehmen und dort die einzelnen Events neue Attribute geben

# TODO Wartezeit naive bestimmen (Aktivitäten sind zeitlich sortiert) oder sicher gehen?
# activitäten nach zeitlichen reihenfolge sortieren?

def _get_next_activity(case:list, activity:dict):
  ''' Sucht die chronologisch nächste Aktivität
  '''
  end = dt.datetime.strptime(activity['end_timestamp'], '%Y-%m-%d %H:%M:%S')
  waiting_time = dt.timedelta(weeks= 10000) # es ist zu erwarten, dass die wartezeit zwischen zwei activitäten weniger als 10000 Wochen sind
  next_act = activity

  for act in case:
    act_endtime = dt.datetime.strptime(act['start_timestamp'], '%Y-%m-%d %H:%M:%S')
    # Aktivität muss NACH unserer kommen
    if act_endtime > end:
      # ist die Wartezeit weniger?
      if waiting_time > end - act_endtime:
        next_act = act
  
  return next_act


def _calculate_case_durations(case:list):
  ''' Berechnet die Zeit eines Cases
  
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

    next_act = _get_next_activity(case, activity)
    if next_act != activity:
      waiting_time += dt.datetime.strptime(activity['end_timestamp'], '%Y-%m-%d %H:%M:%S') - dt.datetime.strptime(next_act['start_timestamp'], '%Y-%m-%d %H:%M:%S')

    # hat eine activität früher angefangen?
    if start_activity < start_time:
      start_time = start_activity
    # hat einen activität später aufgehört?
    if end_activity > end_time:
      end_time = end_activity
   
    activity['duration'] = end_activity - start_activity

  # case sind Listenelemente, dict zuweisung geht nicht
  new_case = {}

  new_case['average_wait'] = waiting_time / (num_acitivties -1) # letzte Aktivität hat keine Wartezeit, daher -1
  new_case['average_act_duration'] = average_duration / num_acitivties
  new_case['activities'] = case
  new_case['duration'] = end_time - start_time

  return new_case

# mutierend
def peformance_for_log(log:dict):
  for case in log.keys():
    log[case] = _calculate_case_durations(log[case])