#!/bin/bash
# Note: 1. you need to have imagemagick installed (sudo apt install imagemagick). 
# 2. the output file or folder should be a relative path, instead of an absolute path. Otherwise, gc3pie will likely not be able to retrieve the output!

IMG=$1
convert /home/ubuntu/tutorial_gc3pie/in-data/$IMG -colorspace gray gray-${IMG}

