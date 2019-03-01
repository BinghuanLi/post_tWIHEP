import sys, os, subprocess
import ROOT
from ROOT import TString, TFile, TTree
from threading import Thread



Categories=["SubCat2l"]
varPerCat={
"SubCat2l":["Bin2l"]
}

version = "V0212"

for category in Categories:
    for var in varPerCat[category]:
        DirName_datacard = version+"_datacards/"+category+"/"+var
        print ( "write txt for var: "+var+ " in cat: "+ category)
        if not os.path.exists(DirName_datacard):
            os.popen("mkdir -p "+DirName_datacard)
        command_run = "python datacard_Template.py -i "+version+"_datacards/ -v "+var+" -c "+category+" > "+DirName_datacard+"/datacard.log"
        print(command_run) 
        os.system(command_run)
