import read_csv as rcsv
import create_graph as cg


log = rcsv.parse_CSV_to_dict('ksv_eventlog_small.csv')

variants = rcsv.get_variants(log)

activities = rcsv.get_activities(log)

print (activities)

paths = []

for v in variants.keys():
  paths.append(v.split())

cg.renderGraph(activities, paths)

