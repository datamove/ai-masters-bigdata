#!/bin/bash

# 1st arg - input path
# 2nd arg - output path
# 3rd arg - files to send with the job
# mapper file

HADOOP_CUR=/usr/hdp/current/
HADOOP_EXE=$HADOOP_CUR/hadoop-client/bin/hadoop
HADOOP_STREAM_JAR=$HADOOP_CUR/hadoop-mapreduce-client/hadoop-streaming.jar
INPUT=$1
OUTPUT=$2
FILES=$3
MAPPER=$4

$HADOOP_EXE jar $HADOOP_STREAM_JAR  -files $FILES -D mapred.reduce.tasks=0 -input $INPUT -output $OUTPUT -mapper $MAPPER

exit

# alternative - local execution
PYTHON_EXE=/opt/conda/envs/dsenv/bin/python

cat $1 | $PYTHON_EXE projects/0/predict.py




