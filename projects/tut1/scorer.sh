#!/bin/bash

# 1st arg - files to send with the job
# 2nd arg - true target path
# 3rd arg - predicted target path
# 4th arg - output path
# 5th arg - reducer file

HADOOP_EXE=/usr/bin/yarn
HADOOP_STREAM_JAR=/usr/lib/hadoop-mapreduce/hadoop-streaming.jar

FILES=$1
INPUT1=$2
INPUT2=$3
OUTPUT=$4
REDUCER=$5

$HADOOP_EXE jar $HADOOP_STREAM_JAR  -files $FILES -D mapred.reduce.tasks=1 -input $INPUT1 -input $INPUT2 -output $OUTPUT -mapper cat -reducer "$REDUCER"




