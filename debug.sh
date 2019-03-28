#!/bin/bash

while true; do

    python -m ptvsd --host 0.0.0.0 --port 3000 --wait -m py

    sleep 1

done
