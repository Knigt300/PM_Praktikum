import read_csv as rcsv


log = rcsv._parse_CSV_to_dict('ksv_eventlog_small.csv')

variants = rcsv._get_variants(log)
