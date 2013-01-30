#! /bin/bash
openssl x509 -req -days $4 -in $2 -signkey $1 -out $3