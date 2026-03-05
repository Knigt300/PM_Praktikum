import datetime as dt


def calculate_waiting_times(case: list):
    ''' Berechnet die Wartezeit zwischen zwei Aktivitäten (mutierend) '''

    zero_time = dt.timedelta(seconds=0)

    
    for i in range(len(case)):

        # Letzte Aktivität hat keine Wartezeit
        if i == len(case) - 1:
            case[i]['wait_time'] = zero_time

        else:
            # Endzeit aktuelles Event
            end_current = dt.datetime.strptime(
                case[i]['end_timestamp'],
                '%Y-%m-%d %H:%M:%S')
            

            # Startzeit nächstes Event
            start_next = dt.datetime.strptime(
                case[i+1]['start_timestamp'],
                '%Y-%m-%d %H:%M:%S')
            

            # Wartezeit
            wait = start_next - end_current

            # Negative Wartezeit verhindern
            if wait > zero_time:
                case[i]['wait_time'] = wait
            else:
                case[i]['wait_time'] = zero_time
                
                
                
                
def calculate_case_metrics(case: list):
    ''' Berechnet Kennzahlen für einen einzelnen Case '''
# Summenvariable auf 0 gesetzt
    total_activity_time = dt.timedelta(seconds=0)
    total_wait_time = dt.timedelta(seconds=0)

    # Erste Startzeit
    first_start = dt.datetime.strptime(
        case[0]['start_timestamp'],
        '%Y-%m-%d %H:%M:%S')
    
    # Späteste Startzeit initialisieren
    last_end = first_start

    
    for event in case:

        
        start = dt.datetime.strptime(event['start_timestamp'], '%Y-%m-%d %H:%M:%S')
        end = dt.datetime.strptime(event['end_timestamp'], '%Y-%m-%d %H:%M:%S')

        # Dauer der Aktivität berechnen
        duration = end - start
        event['duration'] = duration

        total_activity_time += duration
        total_wait_time += event['wait_time']

        # Prüfen, ob diese Aktivität die späteste Endzeit hat
        if end > last_end:
            last_end = end
    # Anzahl Aktivitäten
    num_activities = len(case)
    # Ergebnis Dict.
    result = {}
    # Speicher Resultate, berechnet Durchschnittswerte
    result['activities'] = case
    result['total_duration'] = last_end - first_start
    result['average_activity_duration'] = total_activity_time / num_activities
    result['average_wait_time'] = total_wait_time / (num_activities - 1)
    result['num_activities'] = num_activities

    return result




def performance_log(log: dict):
    ''' Berechnet Durchschnittswerte für das gesamte Log '''
    # Gesamtsummen
    total_act_time = dt.timedelta(seconds=0)
    total_wait_time = dt.timedelta(seconds=0)
    total_activities = 0
    total_waits = 0 

    
    for case_id in log.keys():

        
        if 'KSV' in case_id:

            calculate_waiting_times(log[case_id])  # Wartezeiten berechnen
            log[case_id] = calculate_case_metrics(log[case_id])  # Case-Metriken berechnen

            num_act = log[case_id]['num_activities'] 

            total_activities += num_act  
            total_act_time += log[case_id]['average_activity_duration'] * num_act # Durchschnitt x Anzahl = Gesamtsumme
            total_wait_time += log[case_id]['average_wait_time'] * (num_act - 1) # Wartezeit: Durchschnitt x (Anzahl -1)
            total_waits += (num_act - 1) # Gesamtzeit aller Wartephasen

    # Log-Durchschnittswerte speichern
    log['average_activity_time'] = total_act_time / total_activities
    log['average_wait_time'] = total_wait_time / total_waits
    
    
    
    
def find_bottlenecks(log: dict):
    ''' Sucht Aktivitäten oder Wartezeiten über dem Durchschnitt '''

    problems = []  

    avg_wait = log['average_wait_time']  
    avg_act = log['average_activity_time'] 

    
    for case_id in log.keys():

        if 'KSV' in case_id:

            
            for act in log[case_id]['activities']:

                # Prüfen ob Aktivitätsdauer über Durchschnitt
                if act['duration'] > avg_act:
                    problems.append(('Activity too long',
                                     act['activity'],
                                     act['duration']))

                # Prüfen ob Wartezeit über Durchschnitt
                if act['wait_time'] > avg_wait:
                    problems.append(('Waiting too long',
                                     act['activity'],
                                     act['wait_time']))

    return problems


# Selektiert die längsten Aktivitäten
def get_longest_acts(log: dict, num=1):
    acts = log['average_acts'] # Durchschnittsdaten holen
    
    longest = [] # Speicher längster Aktivitäten

    
    for activity in acts:

        current = (activity, acts[activity]) # Aktuelles Tupel erstellen

        # Wenn Liste noch nicht voll ist dann wird aktuelles Element hinzugefügt
        if len(longest) < num:
            longest.append(current)

        else:
            
            smallest_index = 0 #Startwert erstes Element
            for i in range(len(longest)):
                if longest[i][1] < longest[smallest_index][1]:   # Kleinstes Element in der Liste suchen
                    smallest_index = i

            # Alles was kleiner als die kleinste gespeicherte Dauer ist wird ignoriert
            if current[1] > longest[smallest_index][1]:
                longest[smallest_index] = current


    return longest
