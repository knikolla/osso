#!/usr/bin/env bash
openssl genrsa -out etc/ca.key 4096

openssl req -new -x509 -days 1826 \
    -key etc/ca.key -out etc/ca.crt \
    -subj "/C=US/ST=Denial/L=Springfield/O=Dis/CN=www.example.com"
