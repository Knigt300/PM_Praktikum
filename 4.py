def get_drink_times(log: dict, average=True):
    ''' 
    Analysiert, welches Getränk zu welchem Zeitpunkt des Spiels
    am häufigsten gekauft wird.
    
    Parameters
    ----------
    log: dict
        Das Log mit allen Cases
        
    average: bool
        Wenn True → Durchschnitt pro Match
        Wenn False → Gesamte Anzahl
        
    Returns
    -------
    dict
        Schlüssel: "Getränk - Zeitpunkt"
        Wert: Anzahl bzw. Durchschnitt
    '''

    drinks_per_match = {}

    
    for case in log.keys():
        if 'KSV' in case:

            for act in log[case]['activities']:

                # Nur Getränke-Käufe betrachten
                if act['activity'] == 'getraenk_kaufen':

                    drink = act['object_drink']
                    time = act['object_match_time']
                    match = act['object_match']
                    fan = act['object_fan']

                    key = drink + ' - ' + time  # Kombination aus Getränk & Zeitpunkt

                    # Falls Match schon existiert
                    if match in drinks_per_match:

                        if key in drinks_per_match[match]:
                            drinks_per_match[match][key].append(fan)
                        else:
                            drinks_per_match[match][key] = [fan]

                    else:
                        drinks_per_match[match] = {key: [fan]}

    # Gesamte Anzahl berechnen
    drinks_total = {}

    for match in drinks_per_match.keys():
        for key in drinks_per_match[match].keys():

            if key in drinks_total:
                drinks_total[key] += len(drinks_per_match[match][key])
            else:
                drinks_total[key] = len(drinks_per_match[match][key])

    # Durchschnitt berechnen
    if average:
        num_matches = len(drinks_per_match.keys())

        for key in drinks_total.keys():
            drinks_total[key] = drinks_total[key] / num_matches

    return drinks_total
