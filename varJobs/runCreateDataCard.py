import sys, os, subprocess
import ROOT
from ROOT import TString, TFile, TTree
from threading import Thread



Categories=["SubCat2l"]
varPerCat={
"SubCat2l":["Bin2l","Hj_tagger_resTop"]
}

version = "V0212"

for category in Categories:
    if not os.path.exists("Output/"+category+"/Systs2lss"):
        os.popen("mkdir -p Output/"+category+"/Systs2lss")
        os.popen("mkdir -p Output/"+category+"/SyststtWctrl")
    for var in varPerCat[category]:
        DirName_datacard = version+"_datacards/"+category+"/"+var
        print ( "write histograms for var: "+var+ " in cat: "+ category)
        if not os.path.exists(DirName_datacard):
            os.popen("mkdir -p "+DirName_datacard)
        command_run = "python createDatacardRootFile.py -i Output/SubCat2l/ -o "+DirName_datacard+"/ -v "+var+" -c "+category+" > "+DirName_datacard+"/Information.txt"
        print(command_run) 
        os.system(command_run)
