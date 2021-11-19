#!/bin/bash

set -euf -o pipefail

PROG=snippets.sh

parameters=( \
    "build" \
    "deploy" \
    "test" \
)

usage() {
	echo "usage: $PROG [options]"
    echo
	echo "options:"
	echo "  -h: Show help"
	echo "  -a: Specify an option A"
    echo "  -b: Specify an option B"
	echo "  -p: Specify a parameter"
}

check_parameter() {
    if printf '%s\n' "${parameters[@]}" | grep -qx ${1}; then
        echo "parameter=${1}"
    else
        echo "Invalid parameter=${1}"
        exit 255
    fi
}

func() {
    echo "func ${1}"
}

# Command-line parser 
while getopts ":habp:" opts
do
    case $opts in
        h)
            usage
            ;;
        a)
            FLAG_A=1
            ;;
        b)
            FLAG_B=1
            ;;
        p)
            PARAM=${OPTARG}
            check_parameter ${PARAM}
            ;;
 
    esac
done

shift $((OPTIND - 1))

# Check flags
if [ -n "${FLAG_A}" ]; then
    echo "Set a"
elif [ -n "${FLAG_B}" ];then
    echo "Set b"
else
    echo "Undefined"
fi

func ${PARAM}