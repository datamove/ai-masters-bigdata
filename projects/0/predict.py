#!/opt/conda/envs/dsenv/bin/python

import sys
from joblib import load
import pandas as pd

#load the model
model = load("0.joblib")


fields = """doc_id,hotel_name,hotel_url,street,city,state,country,zip,class,price,
num_reviews,CLEANLINESS,ROOM,SERVICE,LOCATION,VALUE,COMFORT,overall_ratingsource""".replace("\n",'').split(",")

#read and infere
read_opts=dict(
        sep=',', names=fields, index_col=False, header=None,
        iterator=True, chunksize=100
)

for df in pd.read_csv(sys.stdin, **read_opts):
    pred = model.predict(df)
    out = zip(df.doc_id, pred)
    print("\n".join(["{0} {1}".format(*i) for i in out]))

