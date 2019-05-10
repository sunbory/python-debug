#!/bin/bash
#
ROOT_PATH=$(cd $(dirname "$0") && pwd)

export SRC_PATH=${ROOT_PATH}/py
export DIST_PATH=${ROOT_PATH}/dist

export ENTRY_SCRIPT=${SRC_PATH}/__main__.py
export RELEASE="main"

if [ -d ${DIST_PATH} ];then
    echo "delete old dist ${DIST_PATH}"
    rm -rf ${DIST_PATH}
fi

case $1 in
docker)
    docker build -f build/Dockerfile -t python-build  .

    docker run -it --rm -v $(pwd):/opt/ python-build
    ;;
*)    
    pyinstaller -y build/main.spec
    ;;
esac




