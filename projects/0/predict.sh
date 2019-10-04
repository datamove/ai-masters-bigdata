#!/bin/bash

# 1st arg - files to send with the job
# 2nd arg - input path
# 3rd arg - output path
# 4th arg - mapper file

HADOOP_CUR=/usr/hdp/current/
HADOOP_EXE=$HADOOP_CUR/hadoop-client/bin/yarn
HADOOP_STREAM_JAR=$HADOOP_CUR/hadoop-mapreduce-client/hadoop-streaming.jar
FILES=$1
INPUT=$2
OUTPUT=$3
MAPPER=$4

$HADOOP_EXE jar $HADOOP_STREAM_JAR  -files $FILES -D mapred.reduce.tasks=0 -input $INPUT -output $OUTPUT -mapper $MAPPER




