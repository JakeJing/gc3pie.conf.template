#!/bin/bash
# Note: you need to have imagemagick installed (sudo apt install imagemagick). 
IMG=$1
convert /home/ubuntu/tutorial_gc3pie/in-data/$IMG -colorspace gray gray-${IMG}
