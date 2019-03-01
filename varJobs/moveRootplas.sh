#!/bin/bash
list=(
"SigRegion NoJetNCut ttWctrl"
)
for i in $list
do
  mv $i $i\_empty
  mv $i\_empty\/* .
done
