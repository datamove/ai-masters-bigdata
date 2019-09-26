#
# Flask app for Ozonmasters
#
import os
import sys
import json
from flask import Flask
from flask import request, abort, make_response, jsonify, send_from_directory

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Welcome!'

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/sample/<int:proj_id>', methods=['POST'])
def sample(proj_id):
    """Send sampling job 
    Params:
    (proj_id) - homework number
    input path - URI (hdfs or S3 or local etc)
    output path - URI (hdfs or S3 or local etc)
    sampling module  - depends on the lab - MR, Hive, Spark SQL etc
    sampling condition - depends on the lab: python expression, Hive SQL etc.
    
    """
    return exec_script(proj_id, "ozon-masters-bigdata/projects", "sample.sh", request.json)

@app.route('/train/<int:proj_id>', methods=['POST'])
def train_model(proj_id):
    """ Train the model 
    Run a training programm
    It is specific for a homework
    Could be local training job (fork), could be spark submit job,
    Outputs result file in JSON

    Params:
    homework number
    train data URI (HDFS, S3, local etc)
    val(proj_id)ation data URI

    """
    return exec_script(proj_id, "ozon-masters-bigdata/projects", "train.sh", request.json)

def exec_script(proj_id, exec_dir, exec_file, request_json):
    #request_args = json.loads(request_json)
    request_args = request_json
    exec_args = [str(proj_id), *request_args]
    exec_path = "{}/{}/{}".format(exec_dir, proj_id, exec_file)
    print("EXEC_PATH", exec_path)
    print("EXEC_ARGS", exec_args)

    #TODO check if exec_path exists

    newpid = os.fork()
    if newpid == 0:
       os.execl(exec_path, *exec_args)
    return "Ok\n"    


#? upload for checking (test sample is h(proj_id)den)

@app.route('/train_results/<int:proj_id>', methods=['GET'])
def get_train_result(proj_id):
    """ Get JSON with metrics on test data and trained model path.
    Params:
    homework number
     URI (HDFS, S3, local etc)
    """
    return "Ok\n"

#
# Give URI to test data in HDFS or S3
#
@app.route('/predict/<int:proj_id>', methods=['POST'])
def predict(proj_id):
    """ Run inference

    Params:
    homework number
    test data URI
    output data URI

    """
    return exec_script(proj_id, "ozon-masters-bigdata/projects", "predict.sh", request.json)


@app.route('/check/<int:proj_id>', methods=['POST'])
def check(proj_id):
    """ Run a given programm that calculate model metric on a test data set.
    I.e. then run inference job on test data set and save it. 
    Then cal call a programm that compares their prediction with true values.

    How?
    we can let them run a programm via a sticky bit, so they can run it as superuser, 
    but won't be able to see the true data.
    Or
    we can have a microservice that they call with path to their prediction.

    Params:
    homework number
    prediction  data URI

    """
    return



@app.route('/model/<int:proj_id>', methods=['GET'])
def get_model_definition(proj_id):
    """Download a file.
    Download for examination

    Params:
    homework number

    """
    path = "{}.joblib".format(proj_id)
    print("MODEL_FILE", path)
    cwd = os.getcwd()
    print("CWD", cwd)
    from_dir = 'ozon-masters-bigdata/projects/{}'.format(proj_id)
    print("FROM_DIR", from_dir)
    full_path = cwd + "/" + from_dir
    print("FULL_PATH", full_path, file=sys.stderr)
    return send_from_directory(full_path, path, as_attachment=True)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

