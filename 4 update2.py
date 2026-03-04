def analyse_drink_times(log: dict):
    '''
    Analysiert, welches Getränk in welcher Spielphase
    am häufigsten bestellt wurde.
    
    Returns:
        dict: {phase: {getraenk: anzahl}}
    '''

    result = {}

    for case_id in log.keys():

        # Nur echte Match-Cases betrachten
        if 'KSV' in case_id:

            for event in log[case_id]:

                # Nur Getränke-Bestellungen betrachten
                if event['activity'] == 'getraenkestand_bestellen':

                    phase = event['attribute_match_phase']
                    drink = event['attribute_material_type']

                    # Falls Phase noch nicht existiert -> anlegen
                    if phase not in result:
                        result[phase] = {}

                    # Falls Getränk in Phase noch nicht existiert -> anlegen
                    if drink not in result[phase]:
                        result[phase][drink] = 1
                    else:
                        result[phase][drink] += 1


    return result
