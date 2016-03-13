#!/bin/bash
for x in $(cat Crawler/video.txt);do
	$(wget $x);
done
