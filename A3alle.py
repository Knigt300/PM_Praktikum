import datetime as dt


def calculate_waiting_times(case: list):
    ''' Berechnet die Wartezeit zwischen zwei Aktivitäten (mutierend) '''

    zero_time = dt.timedelta(seconds=0)

    
    for i in range(len(case)):

        
        if i == len(case) - 1:
            case[i]['wait_time'] = zero_time

        else:
            
            end_current = dt.datetime.strptime(
                case[i]['end_timestamp'],
                '%Y-%m-%d %H:%M:%S')
            

            
            start_next = dt.datetime.strptime(
                case[i+1]['start_timestamp'],
                '%Y-%m-%d %H:%M:%S')
            

            
            wait = start_next - end_current

            
            if wait > zero_time:
                case[i]['wait_time'] = wait
            else:
                case[i]['wait_time'] = zero_time
                
                
                
                
def calculate_case_metrics(case: list):
    ''' Berechnet Kennzahlen für einen einzelnen Case '''

    total_activity_time = dt.timedelta(seconds=0)
    total_wait_time = dt.timedelta(seconds=0)

    
    first_start = dt.datetime.strptime(
        case[0]['start_timestamp'],
        '%Y-%m-%d %H:%M:%S'
    )

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

    num_activities = len(case)

    result = {}

    result['activities'] = case
    result['total_duration'] = last_end - first_start
    result['average_activity_duration'] = total_activity_time / num_activities
    result['average_wait_time'] = total_wait_time / (num_activities - 1)
    result['num_activities'] = num_activities

    return result




def performance_log(log: dict):
    ''' Berechnet Durchschnittswerte für das gesamte Log '''

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
            total_act_time += log[case_id]['average_activity_duration'] * num_act 
            total_wait_time += log[case_id]['average_wait_time'] * (num_act - 1)
            total_waits += (num_act - 1)

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



def get_longest_acts(log: dict, num=1):
    acts = log['average_acts']

    longest = []

    
    for activity in acts:

        current = (activity, acts[activity])

        
        if len(longest) < num:
            longest.append(current)

        else:
            
            smallest_index = 0
            for i in range(len(longest)):
                if longest[i][1] < longest[smallest_index][1]:
                    smallest_index = i

            
            if current[1] > longest[smallest_index][1]:
                longest[smallest_index] = current


    return longest
