#!/bin/bash

hotel_ids=$1
destination_ids=$2

if [[ -z "$hotel_ids" ]];
then
	echo "ERROR: Hotel ids are empty"
	exit 1
fi

if [[ -z "$destination_ids" ]];
then
	echo "ERROR: Destination ids are empty"
	exit 1
fi

python3 main.py "$1" "$2"
