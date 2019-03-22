#!/bin/bash

ROOT=$(pwd $(cd $(dirname $0)))

fail() {
  local msg=$1
  echo -e "\e[1;31m===> $(date) ERROR: ${msg}\e[0m"
  exit 1
}

# test if there is a rinetd instance
procNum=$(ps afx | grep -v grep | grep './rinetd -c rinetd.conf' | wc -l)
if [[ procNum -gt 0 ]]; then
    fail "rinetd have been installed"
    exit 1
fi

cd $ROOT && ./rinetd -c rinetd.conf

pid=$(ps afx | grep -v grep | grep './rinetd -c rinetd.conf' | awk '{print $1}')

echo $pid > ./pid
