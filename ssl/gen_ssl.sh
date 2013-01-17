#! /bin/bash
NAME=ideco.usagestat
echo KEY GENERATION:
#openssl genrsa -des3 -out $NAME.key 1024
openssl genrsa -out $NAME.key 1024
echo CERTIFICATE SIGNING REQUEST GENERATION:
openssl req -new -key $NAME.key -out $NAME.csr
echo CERTIFICATE GENERATION:
openssl x509 -req -days 10000 -in $NAME.csr -signkey $NAME.key -out $NAME.crt


