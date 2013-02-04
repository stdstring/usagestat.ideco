#! /bin/bash
# check USAGE_STAT_ENABLED variable
if [ "$USAGE_STAT_ENABLED" == "1" ]
then
  python $1
fi