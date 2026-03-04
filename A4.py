def get_drink_metrics(log: dict):
    ''' 
    Analysiert, welches Getränk zu welchem Zeitpunkt des Spiels
    am häufigsten gekauft wird.
    Daten sind nicht einfach anzugucken, es ist empfohlen die Daten
    durch ``filter_drinks`` anschaulicher zu machen.
    
    Parameters
    ----------
    log: dict
        Das Log mit allen Cases
        
        
    Returns
    -------
    dict
        Schlüssel: "Getränk - Zeitpunkt"
        Wert: Anzahl bzw. Durchschnitt
    '''

    # Warum arbeiten wir hier mit match? Wir machen damit nix sinnvolles
    drinks = {}

    
    for case in log.keys():
        if 'KSV' in case:

            for act in log[case]['activities']:

                # Nur Getränke-Käufe betrachten
                # Es wird nie in das if gegangen
                # Aktivitätsname war falsch
                if act['activity'] == 'getraenkestand_bestellen':

                    booth = act['object_stand']
                    time = act['attribute_match_phase']
                    match = act['object_match']
                    

                    key = match + ' - ' + booth + ' - ' + time  # Kombination aus Getränk & Zeitpunkt

                    # Falls Match schon existiert
                    if key in drinks:
                        drinks[key] += 1
                    else:
                        drinks[key] = 1

    return drinks

    
    



# stand, time, match
def filter_drinks(drinks: dict, fltr= 'stand'):
    '''Fitlert Getränkemetrik nach gegebenen Filter

    Paramters
    ---------
    drinks: dict
      Drinkmetric aus ``get_drink_metrics``

    fltr: str
      fltr-Wort, welcher bestimmt, wonach gefiltert wird.
      Zuslässige Filterwörter: ``'stand'``, ``'time'``, ``'match'``
      Bei üngültigem Schlüssel wird ``None`` ausgegeben
    
    Returns
    -------
    Ein Dict, welches die Metrik anhand der Schlüsselwörter sorterit/errechnet hat
    '''
    new_dict = {}
    if fltr == 'stand':
        i = 1
    elif fltr == 'time':
        i = 2
    elif fltr == 'match':
        i = 0
    else:
        return None

    for key in drinks.keys():
      new_key = key.split(' - ')[i]
      if new_key in new_dict:
          new_dict[new_key] += drinks[key]
      else:
          new_dict[new_key] = drinks[key]
    
    return new_dict