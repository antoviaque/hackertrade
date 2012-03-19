#!/bin/bash

for i in `ls orig/homeslide/`; do convert -resize 500 -quality 85 -gravity center -extent 500x330 orig/homeslide/$i $i ; done
for i in `ls orig/team/`; do convert -resize 147 -quality 85 -gravity center -extent 147x110 orig/team/$i $i ; done

