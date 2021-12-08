#!/usr/bin/env bash

day_index=$1
name=$2

print_usage() {
  echo "usage: $0 <day index> <name>"
}
if [ -z "${day_index}" ]; then
    print_usage
    exit 128
fi
if [ -z "${name}" ]; then
    print_usage
    exit 129
fi

mkdir aoc/day"${day_index}"
touch aoc/day"${day_index}"/__init__.py
touch aoc/day"${day_index}"/"${name}".py
mkdir tests/day"${day_index}"
touch tests/day"${day_index}"/__init__.py
touch tests/day"${day_index}"/test_"${name}".py
touch tests/day"${day_index}"/input.txt
