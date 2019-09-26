#!/opt/conda/envs/dsenv/bin/python

import pandas as pd

import os, sys
print (os.getcwd())

from model import model
from sklearn.model_selection import train_test_split
from joblib import dump

proj_id = sys.argv[1] if len(sys.argv)>1 and sys.argv[1] is not None else "0"
train_path = sys.argv[2] if len(sys.argv)>2 and  sys.argv[2] is not None else "ozon-masters-bigdata/projects/0/filtered"
print("TRAIN_ID", proj_id)
print("TRAIN_PATH", train_path)

fields = """doc_id,hotel_name,hotel_url,street,city,state,country,zip,class,price,
num_reviews,CLEANLINESS,ROOM,SERVICE,LOCATION,VALUE,COMFORT,overall_ratingsource""".replace("\n",'').split(",")

read_table_opts = dict(sep=",", names=fields, index_col=False)
df = pd.read_table(train_path, **read_table_opts)

#split train/val
X_train, X_test, y_train, y_test = train_test_split(
    df.iloc[:,:-1], df.iloc[:,-1], test_size=0.33, random_state=42
)

model.fit(X_train, y_train)
print("model score: %.3f" % model.score(X_test, y_test))

# save the model
dump(model, "{}.joblib".format(proj_id))

