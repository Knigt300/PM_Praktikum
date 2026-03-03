import read_csv as rcsv
import folgerungsgraphminer as fgm
import datetime as dt
import performance as p

log = rcsv.parse_CSV_to_dict('ksv_eventlog_small.csv')


folerungsgraph = fgm.Folgerungsgraph(log)

folerungsgraph.drawFolgerungsgraph()

p.peformance_for_log(log)

long_cases = p.get_longest_cases(log, 3)
print('Längsten Fälle:')
for case in long_cases:
  print(case['activities'][0]['case_id'],case['duration'])

bottlenecks = p.get_bottlenecks(log)
print(log['average_dur_act'], log['average_dur_wait'])
print('Durchschnittliche Wartezeit:', bottlenecks['threshhold_wait'])
print('Durchschnittliche Aktivitätesdauer:', bottlenecks['threshhold_act'])

for acts in bottlenecks['problems']:
  if ' ' in acts[0]:
    print('Wartezeit:', acts[1], 'von', acts[0].split()[0],'zu', acts[0].split()[1])
  else:
    print('Prozessdauer:', acts[1], 'von', acts[0])

long_acts = p.get_longest_acts(log, 5)
for (path, dur) in long_acts:
  print(path, dur)