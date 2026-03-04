def get_drink_stand_activity(log: dict, average=True):
    '''
    Berechnet die Auslastung der Getränkestände pro Match.
    
    Dabei werden die Bestellungen der Getränke als Metrik benutzt.

    Parameters
    ----------
    log: dict
        Das Log, in welchem die Daten sind.
    average: bool
        Wenn True → Durchschnitt pro Match, sonst totale Anzahl

    Returns
    -------
    dict
        Schlüssel: Getränk + Stand + Spielphase
        Wert: Anzahl (oder Durchschnitt) der Bestellungen
    '''

    drinks_per_match = {}

    for case in log.keys():
        if 'KSV' in case:  # Nur echte Matches
            for act in log[case]['activities']:

                # Nur Getränke-Bestellungen berücksichtigen
                if act['activity'] == 'getraenkestand_bestellen':

                    drink = act['attribute_material_type']      # Getränk
                    stand = act['object_stand']                 # Stand
                    phase = act['attribute_match_phase']        # Spielphase
                    match = act['object_match']                 # Match
                    fan = act['object_fan']                     # Fan-ID

                    # Kombinierter Schlüssel: Getränk + Stand + Phase
                    key = f"{drink} - {stand} - {phase}"

                    # Match bereits vorhanden?
                    if match in drinks_per_match:
                        if key in drinks_per_match[match]:
                            drinks_per_match[match][key].append(fan)
                        else:
                            drinks_per_match[match][key] = [fan]
                    else:
                        drinks_per_match[match] = {key: [fan]}

    # Gesamtauslastung berechnen
    drinks_total = {}

    for match in drinks_per_match.keys():
        for key in drinks_per_match[match].keys():
            if key in drinks_total:
                drinks_total[key] += len(drinks_per_match[match][key])
            else:
                drinks_total[key] = len(drinks_per_match[match][key])

    # Durchschnitt pro Match berechnen
    if average:
        num_matches = len(drinks_per_match.keys())
        for key in drinks_total.keys():
            drinks_total[key] = drinks_total[key] / num_matches

    return drinks_total


