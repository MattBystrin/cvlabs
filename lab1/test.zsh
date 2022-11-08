#!/bin/zsh

timeraw=0

for i in {1..100}
do
	t=$(eval $1)
	(( timeraw+=t ))
done

((timeraw/=100))

echo $timeraw
