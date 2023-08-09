#!/bin/bash

directory_path=$1

find "$directory_path" -type f -mmin +1 -exec rm {} \;