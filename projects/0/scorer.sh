#!/bin/bash

# 1st arg - true target path
# 2nd arg - predicted target path
# 3rd     - score output path
# 4rd arg - files to send with the job
# reducer file

HADOOP_CUR=/usr/hdp/current/
HADOOP_EXE=$HADOOP_CUR/hadoop-client/bin/hadoop
HADOOP_STREAM_JAR=$HADOOP_CUR/hadoop-mapreduce-client/hadoop-streaming.jar
INPUT1=$1
INPUT2=$2
OUTPUT=$3
FILES=$4
REDUCER=$5

$HADOOP_EXE jar $HADOOP_STREAM_JAR  -files $FILES -D mapred.reduce.tasks=1 -input $INPUT1 -input $INPUT2 -output $OUTPUT -mapper cat -reducer $REDUCER




