#!/bin/bash

BASEDIR=$(dirname "$0")
cd "${BASEDIR}" || exit 1
BASEDIR=$(pwd)

source config.sh
if [ -f config/config_local.sh ]; then
    source config/config_local.sh
fi

set -x

if [ ! -d "${UPSTREAM_DIR}" ]; then
    git clone --depth=1 "${UPSTREAM_REPO}" "${UPSTREAM_DIR}"
fi

if [ ! -d "${PMC_DIR}" ]; then
    git clone --depth=1 "${PMC_REPO}" "${PMC_DIR}"
fi
