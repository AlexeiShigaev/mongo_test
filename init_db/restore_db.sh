#!/bin/bash

echo "!!! mongorestore !!!"
cd /docker-entrypoint-initdb.d/
mongorestore --uri mongodb://127.0.0.1:27017 --nsInclude="sampleDB.*" dump
