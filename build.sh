#!/bin/bash

cd static
for i in `ls body/` ; do cat header.html body/$i footer.html > $i ; done

cd img
./convert.sh

