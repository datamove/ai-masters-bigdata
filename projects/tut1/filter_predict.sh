#!/bin/bash

#HADOOP_CUR=/usr/hdp/current/
#HADOOP_EXE=$HADOOP_CUR/hadoop-client/bin/yarn
#HADOOP_STREAM_JAR=$HADOOP_CUR/hadoop-mapreduce-client/hadoop-streaming.jar
HADOOP_EXE=/usr/bin/yarn
HADOOP_STREAM_JAR=/usr/lib/hadoop-mapreduce/hadoop-streaming.jar

FILES=$1
INPUT=$2
OUTPUT=$3
MAPPER=$4
REDUCER=$5
$HADOOP_EXE jar $HADOOP_STREAM_JAR  -files $FILES -input $INPUT -output $OUTPUT -mapper "$MAPPER" -reducer "$REDUCER"


