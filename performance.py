import datetime as dt

# log aus aufgabe 1 bearbeiten/erweitern
# einen case nehmen und dort die einzelnen Events neue Attribute geben

# TODO Wartezeit naive bestimmen (Aktivitäten sind zeitlich sortiert) oder sicher gehen?


def _modify_log_numActivities_per_case(log:dict):
  for case in log.keys():
    case['num_activities'] = len(log[case])

def _calculate_case_duration(case:list):

  start_time = dt.datetime.strptime(case[0]['start_timestamp'], '%Y-%m-%d %H:%M:%S')
  end_time = dt.datetime.strptime(case[0]['end_timestamp'], '%Y-%m-%d %H:%M:%S')
  for activity in case:
    start_activity = dt.datetime.strptime(activity['start_timestamp'])
    end_activity = dt.datetime.strptime(activity['end_timestamp'])
    # hat eine activität früehr angefangen?
    if start_activity < start_time:
      start_time = start_activity
    # hat eien activität später aufgehört?
    if end_activity > end_time:
      end_time = end_activity
   
    activity['duration'] = end_activity - start_activity
  
  case['duration'] = end_time - start_time