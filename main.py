import read_csv as rcsv
import folgerungsgraphminer as fgm
import datetime as dt
import performance as p

log = rcsv.parse_CSV_to_dict('ksv_eventlog_small.csv')

#  TODO case in dict umwandeln damit Platz für Metriken ist


start_time = dt.datetime.strptime(log['KSV0000001'][0]['start_timestamp'], "%Y-%m-%d %H:%M:%S")
end_time = dt.datetime.strptime(log['KSV0000001'][0]['end_timestamp'], "%Y-%m-%d %H:%M:%S")
print(start_time)
print(end_time)
print(end_time - start_time)
buff = dt.timedelta(seconds=  end_time.timestamp() - start_time.timestamp())
print(buff/2)

variants = rcsv.get_variants(log)

activities = rcsv.get_activities(log)

p.peformance_for_log(log)
# folerungsgraph = fgm.Folgerungsgraph(activities, variants)

# folerungsgraph.drawFolgerungsgraph()



