#! /bin/bash
date --date="$(openssl x509 -in $1 -noout -enddate | cut -d= -f 2)" --iso-8601