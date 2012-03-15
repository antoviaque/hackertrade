#!/bin/bash

for i in `ls orig/`; do convert -resize 500 -quality 95 -gravity center -extent 500x330 orig/$i $i ; done
