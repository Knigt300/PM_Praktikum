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
print('Durchschnittliche Wartezeit:', bottlenecks['threshhold'])

for acts in bottlenecks['problems']:
  print('Wartezeit:', acts[1], 'von', acts[0].split()[0],'zu', acts[0].split()[1])
