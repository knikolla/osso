#!/usr/bin/env bash
docker run -d -p 5000:5000 -v `pwd`/etc:/etc/osso --name osso osso
