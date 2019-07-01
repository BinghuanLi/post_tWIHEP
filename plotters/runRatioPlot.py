import sys, os, subprocess
import ROOT
from ROOT import TString, TFile, TTree
from threading import Thread


Categories=["SubCat2l","DNNCat","DNNCat_option2","DNNCat_option3","DNNSubCat1_option1","DNNSubCat1_option2","DNNSubCat1_option3","DNNSubCat2_option1","DNNSubCat2_option2","DNNSubCat2_option3"]
#Categories=["SubCat2l","DNNCat","DNNCat_option2","DNNCat_option3"]

varPerCat={
"SubCat2l":["Bin2l"],
"DNNCat":["DNN_maxval"],
"DNNCat_option2":["DNN_maxval_option2"],
"DNNCat_option3":["DNN_maxval_option3"],
"DNNSubCat1_option1":["DNN_maxval"],
"DNNSubCat1_option2":["DNN_maxval_option2"],
"DNNSubCat1_option3":["DNN_maxval_option3"],
"DNNSubCat2_option1":["DNN_maxval"],
"DNNSubCat2_option2":["DNN_maxval_option2"],
"DNNSubCat2_option3":["DNN_maxval_option3"],
}

# show 2lss for the moment
regPerCat={
"SubCat2l":["2lss"],
"DNNCat":["2lss"],
"DNNCat_option2":["2lss"],
"DNNCat_option3":["2lss"],
"DNNSubCat1_option1":["2lss"],
"DNNSubCat1_option2":["2lss"],
"DNNSubCat1_option3":["2lss"],
"DNNSubCat2_option1":["2lss"],
"DNNSubCat2_option2":["2lss"],
"DNNSubCat2_option3":["2lss"],
}

dirName = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/CombineStuff/CMSSW_8_1_0/src/HiggsAnalysis/V0321_loose/V0321_loose_datacards_All/"

blind ="1"
latex ="1"
fit = "prefit"

for category in Categories:
    for var in varPerCat[category]:
        print ( "plot var: "+var+ " in cat: "+ category)
        for reg in regPerCat[category]:
            command_run = "python ratioplot.py -r "+reg+" -p "+var+" -c "+category+" -d "+dirName + " -l "+latex+" -f "+fit + " -b "+ blind 
            print(command_run) 
            os.system(command_run)
