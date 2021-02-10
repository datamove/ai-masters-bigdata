#!/opt/conda/envs/dsenv/bin/python

#
# This is a MAE scorer
#

import sys
import os
from glob import glob
import logging
import math

#
# Init the logger
#
logging.basicConfig(level=logging.DEBUG)
logging.info("CURRENT_DIR {}".format(os.getcwd()))
logging.info("SCRIPT CALLED AS {}".format(sys.argv[0]))
logging.info("ARGS {}".format(sys.argv[1:]))

score = 0
n_records = 0


prev_key = None
values = []

for line in sys.stdin:
    key, value = line.strip().split(",")

    if key != prev_key and prev_key is not None:
        score += math.fabs(values[0] - values[1])
        n_records += 1
        values = []
    values.append(float(value))
    prev_key = key

if prev_key is not None:
    score += math.fabs(values[0] - values[1])
    n_records += 1

score /= n_records

print(score)

sys.exit(0)



