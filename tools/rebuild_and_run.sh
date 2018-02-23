#!/usr/bin/env bash
docker stop osso
docker rm osso
docker build -t osso .
docker run -d -p 5000:5000 -v `pwd`/etc:/etc/osso --name osso osso
