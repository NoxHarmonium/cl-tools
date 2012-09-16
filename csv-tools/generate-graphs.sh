#!/bin/bash

./generate-graph.py -v 0,1 header.def ./hv-0.gplot ~/Study/results130912/{1,6,11,16,21,26,31,36}.csv
./generate-graph.py -v 0,1 header.def ./hv-1.gplot ~/Study/results130912/{2,7,12,17,22,27,32,37}.csv
./generate-graph.py -v 0,1 header.def ./hv-2.gplot ~/Study/results130912/{3,8,13,18,23,28,33,38}.csv
./generate-graph.py -v 0,1 header.def ./hv-3.gplot ~/Study/results130912/{4,9,14,19,24,29,34,39}.csv
./generate-graph.py -v 0,1 header.def ./hv-4.gplot ~/Study/results130912/{5,10,15,20,25,30,35,40}.csv


