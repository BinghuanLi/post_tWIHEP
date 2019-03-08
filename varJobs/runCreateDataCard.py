import sys, os, subprocess
import ROOT
from ROOT import TString, TFile, TTree
from threading import Thread



Categories=["SubCat2l","DNNCat","DNNCat_option2","DNNCat_option3","DNNSubCat1_option1","DNNSubCat1_option2","DNNSubCat1_option3","DNNSubCat2_option1","DNNSubCat2_option2","DNNSubCat2_option3"]
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

version = "V0307_fakeable"

for category in Categories:
    if not os.path.exists("Output/"+category+"/Systs2lss"):
        os.popen("mkdir -p Output/"+category+"/Systs2lss")
        os.popen("mkdir -p Output/"+category+"/SyststtWctrl")
    for var in varPerCat[category]:
        DirName_datacard = version+"_datacards/"+category+"/"+var
        print ( "write histograms for var: "+var+ " in cat: "+ category)
        if not os.path.exists(DirName_datacard):
            os.popen("mkdir -p "+DirName_datacard)
        command_run = "python createDatacardRootFile.py -i Output/"+category+"/ -o "+DirName_datacard+"/ -v "+var+" -c "+category+" > "+DirName_datacard+"/Information.txt"
        print(command_run) 
        os.system(command_run)
