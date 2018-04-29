#!/bin/bash
openssl genrsa -out ca.key
openssl req -x509 -key ca.key -out ca.crt
openssl genrsa -out ppp.key 2048
openssl req -new -key ppp.key -out ppp.csr
openssl x509 -req -in ppp.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out ppp.crt -sha256
