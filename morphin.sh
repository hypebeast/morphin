#!/bin/sh

PROGRAM_DIR=$(dirname $0)

cd ${PROGRAM_DIR}
exec python morphin.py "$@"