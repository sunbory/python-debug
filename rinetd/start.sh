#!/bin/bash

ROOT=$(pwd $(cd $(driname $0)))

cd $ROOT && ./rinetd -c rinetd.conf

echo $$ > ./pid
