import read_csv as rcsv
import folgerungsgraphminer as fgm
import datetime as dt
import performance as p
import analyse as anal
import A4

log = rcsv.parse_CSV_to_dict('ksv_eventlog_small.csv')


# folerungsgraph = fgm.Folgerungsgraph(log)

# folerungsgraph.drawFolgerungsgraph()

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

# Wie sehr sind die Gates im Schnitt ausgelastet?
gates = list(anal.get_gate_activity(log, average= True).items())

gates.sort(key = lambda x: x[1])

sum_entry = 0
sum_exit = 0

for g in gates:
  if 'exit' in g[0]:
    sum_exit += g[1]
  else:
    sum_entry += g[1]
  print(g[0], g[1])

print('Eintritte:', sum_entry)
print('Austritte:', sum_exit)


'''
Auffälligkeit: Nicht alle Menschen verlassen das Stadion

Grund anhand des Graphes erkannt:
Menschen fliegen während der Kontrolle raus, dies passiert erst, nachdem sie ihr Ticket gescannt haben.
'''

drinks = A4.get_drink_metrics(log)
for m in drinks.keys():
    print(m, drinks[m])

stands = A4.filter_drinks(drinks, 'stand')
time = A4.filter_drinks(drinks, 'time')
game = A4.filter_drinks(drinks, 'match')
# Wie viele Stände gibt es pro Bereich?
n,o,s,w = 0,0,0,0
# Getränke pro Bereich
nd, od, sd, wd = 0,0,0,0

# 'N' ist in jedem Schlüssel, daher mit '_N_' nach Bereich gucken
for key in stands.keys():
  if '_N_' in key:
    n += 1
    nd += stands[key]
  elif '_E_' in key:
    o += 1
    od += stands[key]
  elif '_S_' in key:
    s += 1
    sd += stands[key]
  elif '_W_':
    w += 1
    wd += stands[key]
  print(key, stands[key])

for key in time.keys():
  print(key, time[key])

for key in game.keys():
  print(key, game[key])

print('Norden: Stände:',n,'Getränke:',nd,'Durchschnitt:',nd/n)
print('Osten: Stände:',o,'Getränke:',od,'Durchschnitt:',od/o)
print('Süden: Stände:',s,'Getränke:',sd,'Durchschnitt:',sd/s)
print('Westen: Stände:',w,'Getränke:',wd,'Durchschnitt:',wd/w)

'''
Auffälliges: Es werden viele Getränke nach dem Spiel gekauft


Als Person, die Fußball nicht verfolgt, sind erstaunlich wenig Getränke vorm Start geholt worden

Pro Match Metrik müsste man mit Anzahl Besuchern abgleichen, damit diese aussagekräftig ist

Der Süden ist im Verhältniss zum Rest sehr ausgelastet. Dies kann ein Problem sein, wenn Leute lange warten müssen.
Wir haben aber nicht die Anstellzeit in unserem Log.

'''