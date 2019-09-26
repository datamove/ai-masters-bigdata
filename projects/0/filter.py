#!/opt/conda/envs/dsenv/bin/python

import sys
import os

exec(open("filter_cond.py").read())

fields = """doc_id,hotel_name,hotel_url,street,city,state,country,zip,class,price,
num_reviews,CLEANLINESS,ROOM,SERVICE,LOCATION,VALUE,COMFORT,overall_ratingsource""".replace("\n",'').split(",")

for line in sys.stdin:
    # skip header
    if line.startswith(fields[0]):
        continue

    #unpack into a tuple/dictq
    values = line.rstrip().split(',')
    hotel_record = dict(zip(fields, values)) #Hotel(values)

    #apply filter conditions
    if filter_cond(hotel_record):
        #rstrips neede to fix some end line discrepancies
        print(line.rstrip().rstrip(','))



