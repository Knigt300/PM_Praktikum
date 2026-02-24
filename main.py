import read_csv as rcsv
import folgerungsgraphminer as fgm


log = rcsv.parse_CSV_to_dict('ksv_eventlog_small.csv')

variants = rcsv.get_variants(log)

activities = rcsv.get_activities(log)

folerungsgraph = fgm.Folgerungsgraph(activities, variants)

folerungsgraph.drawFolgerungsgraph()



