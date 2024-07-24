#!/bin/bash

while getopts c:s flag
do
    case "${flag}" in
        c) config_file=${OPTARG};;
    esac
done

./venv/bin/python3 main.py -c $config_file