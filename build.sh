#!/bin/bash
#

repo_url=https://github.com/sunbory/pybuild/archive/master.zip
if ! curl -fsSL -o "pypuild.zip" "${repo_url}"; then
    fail "failed to download pypuild binary from ${repo_url}"
fi
