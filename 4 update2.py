def get_drink_stand_usage(log: dict):
    '''
    Analysiert die Auslastung der Getränke pro Stand.
    Für jedes Getränk, jeden Stand und jede Spielphase wird gezählt,
    wie oft das Getränk bestellt wurde.

    Returns:
        dict: {stand: {phase: {getraenk: anzahl}}}
    '''

    usage = {}

    for case_id in log.keys():

        if 'KSV' in case_id:  # nur echte Matches

            for event in log[case_id]:

                # Nur Getränke-Bestellungen berücksichtigen
                if event['activity'] == 'getraenkestand_bestellen':

                    stand = event['object_stand']  # Stand-Name
                    phase = event['attribute_match_phase']  # Spielphase
                    drink = event['attribute_material_type']  # Getränk

                    # Stand anlegen, falls noch nicht vorhanden
                    if stand not in usage:
                        usage[stand] = {}

                    # Phase im Stand anlegen
                    if phase not in usage[stand]:
                        usage[stand][phase] = {}

                    # Getränk in der Phase zählen
                    if drink not in usage[stand][phase]:
                        usage[stand][phase][drink] = 1
                    else:
                        usage[stand][phase][drink] += 1

    return usage

