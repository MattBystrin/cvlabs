#!/bin/bash

#Script generates pair of images where used 2 different algorithm

sources="cup corners" # corners circuit"
for src in $sources
do
	tpls="$(ls img/ | grep _$src)"
	echo $tpls
	for tpl in $tpls
	do
		./pmatch.py -t orb img/$tpl img/$src.jpg -o img/baked/orb_$tpl
		./pmatch.py -t pmatch img/$tpl img/$src.jpg -o img/baked/m_$tpl
	done
done

