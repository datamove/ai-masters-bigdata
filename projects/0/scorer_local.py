#!/opt/conda/envs/dsenv/bin/python

#
# This is a MAE scorer
#

import sys
import os
import logging
import pandas as pd
from sklearn.metrics import mean_absolute_error

#
# Init the logger
#
logging.basicConfig(level=logging.DEBUG)
logging.info("CURRENT_DIR {}".format(os.getcwd()))
logging.info("SCRIPT CALLED AS {}".format(sys.argv[0]))
logging.info("ARGS {}".format(sys.argv[1:]))

#
# Read true values
#
try:
    true_path, pred_path = sys.argv[1:]
except:
    logging.critical("Parameters: true_path (local) and pred_path (url or local)")
    sys.exit(1)

logging.info(f"TRUE PATH {true_path}")
logging.info(f"PRED PATH {pred_path}")


#open true path
df_true = pd.read_csv(true_path, header=None, index_col=0, names=["id", "true"])

#open pred_path
df_pred = pd.read_csv(pred_path, header=None, index_col=0, names=["id", "pred"])

len_true = len(df_true)
len_pred = len(df_pred)

logging.info(f"TRUE RECORDS {len_true}")
logging.info(f"PRED RECORDS {len_pred}")

assert len_true == len_pred, f"Number of records differ in true and predicted sets"

df = df_true.join(df_pred)
len_df = len(df)
assert len_true == len_df, f"Konined true and pred has different number of records: {len_df}"

score = mean_absolute_error(df['true'], df['pred'])

print(score)

sys.exit(0)



