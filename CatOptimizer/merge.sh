#!/bin/bash
list=(
"SigRegion ttWctrl"
)
for i in $list
do
  cd $i
  hadd -f TTH_$i\.root TTH_h*root
  rm TTH_h*.root
  hadd -f Rest_$i\.root TH?_*.root EWK_*.root TTWW_*.root Rares_*.root
  rm TH?_*.root
  rm EWK_*.root
  rm TTWW_*.root
  rm Rares_*.root
  cd ..
done
