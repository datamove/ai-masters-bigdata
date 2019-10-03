#!/bin/bash

HADOOP_CUR=/usr/hdp/current/
HADOOP_EXE=$HADOOP_CUR/hadoop-client/bin/hadoop
HADOOP_STREAM_JAR=$HADOOP_CUR/hadoop-mapreduce-client/hadoop-streaming.jar
INPUT=$1
OUTPUT=$2
FILES=$3
MAPPER=$4
$HADOOP_EXE jar $HADOOP_STREAM_JAR  -files $FILES -D mapred.reduce.tasks=0 -input $INPUT -output $OUTPUT -mapper "$MAPPER"


