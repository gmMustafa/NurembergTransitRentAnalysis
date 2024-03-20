#!/bin/bash -x

echo "=== Executing pipeline ==="
# Execute your pipeline
#python project/data/pipeline.py
python pipeline.py

echo "=== Extracting  LAT LNG ==="
#python project/LatLngExtractor.py
python LatLngExtractor.py

read -p "Press any key to continue... " -n1 -s
exit 0
