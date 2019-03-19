#!/bin/bash

DATACARD="ttH_2lss_ttWctrl"
MASS="125"

if [ "$1" != "" ]; then
    DATACARD=${1}
fi

echo "Preliminary: convert to rootspace"
echo "---------------------------------"

rm ${DATACARD}.root
echo ${DATACARD}.txt
text2workspace.py ${DATACARD}.txt -m ${MASS}
DATACARD="${DATACARD}.root"

echo "First Stage: fit for each POI"
echo "-----------------------------"

combineTool.py -M Impacts -d ${DATACARD} -m ${MASS} --doInitialFit --robustFit 1 --expectSignal 1 -t -1


echo "Second Stage: fit scan for each nuisance parameter"
echo "--------------------------------------------------"

combineTool.py -M Impacts -d ${DATACARD} -m ${MASS} --robustFit 1 --doFits --parallel 8 --expectSignal 1 -t -1

echo "Third Stage: collect outputs"
echo "----------------------------"

combineTool.py -M Impacts -d ${DATACARD} -m ${MASS} -o impacts_exp.json --expectSignal 1 -t -1

echo "Fourth Stage: plot pulls and impacts"
echo "------------------------------------"

plotImpacts.py -i impacts_exp.json -o impacts_exp

exit 0
