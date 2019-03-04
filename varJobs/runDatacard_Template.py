import sys, os, subprocess
import ROOT
from ROOT import TString, TFile, TTree
from threading import Thread


Categories=["SubCat2l","DNNCat","DNNCat_option2","DNNCat_option3"]
varPerCat={
"SubCat2l":["Bin2l"],
"DNNCat":["DNN_maxval"],
"DNNCat_option2":["DNN_maxval_option2"],
"DNNCat_option3":["DNN_maxval_option3"],
}

version = "V0227"

for category in Categories:
    for var in varPerCat[category]:
        DirName_datacard = version+"_datacards/"+category+"/"+var
        print ( "write txt for var: "+var+ " in cat: "+ category)
        if not os.path.exists(DirName_datacard):
            os.popen("mkdir -p "+DirName_datacard)
        command_run = "python datacard_Template.py -i "+version+"_datacards/ -v "+var+" -c "+category+" > "+DirName_datacard+"/datacard.log"
        print(command_run) 
        os.system(command_run)
