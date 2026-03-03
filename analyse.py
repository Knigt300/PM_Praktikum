def get_gate_activity(log:dict, average = True):
  ''' Erechnet die Auslastung der Gates pro Match
  
  Dabei werden die gescannten Tickets als Metrik benutzt 

  Parameters
  ----------
  log: dict
    Das Log in welchem die Daten sind.

  average = True
    Bestimmt ob der Durchschnitt oder die totale Anzahl ausgegeben wird
  
  Returns
  -------
  Ein dict welches als Schlüssel die Matches hat und dann ein dict hat,
    welches Auslastung pro Gate hat. Es wird sich gemerkt, welcher Fan wo rein/raus geht
  '''

  gates_per_match = {}
  for case in log.keys():
    if 'KSV' in case:
      for act in log[case]['activities']:

        if act['activity'] == 'einlass_ticket_scannen' or act['activity'] == 'auslass_ticket_scannen':
          gate = act['object_gate'] + ' entry' if act['activity'] == 'einlass_ticket_scannen' else act['object_gate'] + ' exit'
          fan = act['object_fan']
          match = act['object_match']
          # ist Match schon vorhanden?
          if match in gates_per_match:
            # habe ich schon das Gate als eintritt?
            if gate in gates_per_match[match]:
              gates_per_match[match][gate].append(fan)
            else:
              gates_per_match[match][gate] = [fan]
          else:
            gates_per_match[match] = {gate: [fan]}
  

  gates = {}

  # totale Anzahl berechnen
  for match in gates_per_match.keys():
    for gate in gates_per_match[match].keys():
      if gate in gates:
        gates[gate] += len(gates_per_match[match][gate])
      else:
        gates[gate] = len(gates_per_match[match][gate])

  # wenn Durchschnitt berechnen werden soll
  if average:
    num_matches = len(gates_per_match.keys())
    for gate in gates.keys():
      gates[gate] = gates[gate] / num_matches


  return gates

