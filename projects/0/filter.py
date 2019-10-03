#!/opt/conda/envs/dsenv/bin/python

import sys
import os
from glob import glob
import logging

#
# Init the logger
#
logging.basicConfig(level=logging.DEBUG)
logging.info("CURRENT_DIR {}".format(os.getcwd()))
logging.info("SCRIPT CALLED AS {}".format(sys.argv[0]))
logging.info("ARGS {}".format(sys.argv[1:]))

#
# import the filter
#
filter_cond_files = glob('filter_cond*.py')
logging.info(f"FILTERS {filter_cond_files}")

if len(filter_cond_files) != 1:
    logging.critical("Must supply exactly one filter")
    sys.exit(1)

exec(open(filter_cond_files[0]).read())

#
# dataset fields
#
fields = """doc_id,hotel_name,hotel_url,street,city,state,country,zip,class,price,
num_reviews,CLEANLINESS,ROOM,SERVICE,LOCATION,VALUE,COMFORT,overall_ratingsource""".replace("\n",'').split(",")

#
# Optional argument
# If +field option is given, output the id (always first record) and the given field
# if -field is given, output all but the given field
#

if len(sys.argv) == 1:
  #by default print all fields
  outfields = fields
else:
  op, field = sys.argv[1][0], sys.argv[1][1:]
  logging.info(f"OP {op}")
  logging.info(f"FIELD {field}")

  if not op in "+-" or not field in fields:
    logging.critical("The optional argument must start with + or - followed by a valid field")
    sys.exit(1)
  elif op == '+':
    outfields = [fields[0], field]
  else:
    outfields = list(fields) # like deepcopy, but on the first level only!
    outfields.remove(field)



for line in sys.stdin:
    # skip header
    if line.startswith(fields[0]):
        continue

    #unpack into a tuple/dict
    values = line.rstrip().split(',')
    hotel_record = dict(zip(fields, values)) #Hotel(values)

    #apply filter conditions
    if filter_cond(hotel_record):
        output = ",".join([hotel_record[x] for x in outfields])
        print(output)



