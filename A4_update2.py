def get_block_activity(log: dict, average=True):
    '''
    Berechnet die Auslastung der Tribünenblöcke pro Match.
    
    Dabei werden die gescannten Eintrittstickets als Metrik benutzt.

    Parameters
    ----------
    log: dict
        Das Log in welchem die Daten sind.
    average: bool
        Wenn True → Durchschnitt pro Match
        Wenn False → totale Anzahl

    Returns
    -------
    dict
        Schlüssel: Block
        Wert: Anzahl (oder Durchschnitt) der Fans
    '''

    blocks_per_match = {}

    for case in log.keys():
        if 'KSV' in case:  # nur echte Matches

            for act in log[case]['activities']:

                # Nur Eintritt scannen betrachten
                if act['activity'] == 'einlass_ticket_scannen':

                    block = act['object_block']
                    fan = act['object_fan']
                    match = act['object_match']

                    # Struktur aufbauen
                    if match in blocks_per_match:

                        # Fan zum Block hinzufügen / Block hinzufügen
                        if block in blocks_per_match[match]:
                            blocks_per_match[match][block].append(fan)
                        else:
                            blocks_per_match[match][block] = [fan]

                    else:
                        blocks_per_match[match] = {block: [fan]}

    # Gesamtauslastung berechnen
    blocks_total = {}

    for match in blocks_per_match.keys():
        for block in blocks_per_match[match].keys():

            if block in blocks_total:
                blocks_total[block] += len(blocks_per_match[match][block])
            else:
                blocks_total[block] = len(blocks_per_match[match][block])



    return blocks_total

