import sys, os, subprocess
import ROOT
from ROOT import TString, TFile, TTree
from threading import Thread


Categories=["SubCat2l","DNNCat","DNNCat_option2","DNNCat_option3","DNNAMS2Cat1_option1","DNNAMS2Cat1_option2","DNNAMS2Cat1_option3","DNNAMS3Cat1_option1","DNNAMS3Cat1_option2","DNNAMS3Cat1_option3"]
#Categories=["SubCat2l","DNNCat","DNNCat_option2","DNNSubCat1_option1","DNNSubCat1_option2","DNNSubCat2_option1","DNNSubCat2_option2"]
#Categories=["DNNCat_option2"]
Uncs = ["All","NoStat","NoSyst","None","NoShape"]
#Uncs = ["NoShape"]
Opts = {
"All":" ",
"NoStat":" -m ",
"NoSyst":" -s ",
"NoShape":" -t ",
"None":" -s -m ",
}
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
"DNNAMS2Cat1_option1":["DNN_maxval"],
"DNNAMS2Cat1_option2":["DNN_maxval_option2"],
"DNNAMS2Cat1_option3":["DNN_maxval_option3"],
"DNNAMS3Cat1_option1":["DNN_maxval"],
"DNNAMS3Cat1_option2":["DNN_maxval_option2"],
"DNNAMS3Cat1_option3":["DNN_maxval_option3"],
}

version = "V0321_loose_AMSBin"


for Unc in Uncs:
    command_cp = "cp -r "+version+"_datacards "+version+"_datacards_"+Unc
    print(command_cp)
    os.system(command_cp)
    for category in Categories:
        for var in varPerCat[category]:
            DirName_datacard = version+"_datacards_"+Unc+"/"+category+"/"+var
            print ( "write txt for var: "+var+ " in cat: "+ category)
            if not os.path.exists(DirName_datacard):
                os.popen("mkdir -p "+DirName_datacard)
            command_run = "python datacard_Template.py -i "+version+"_datacards_"+Unc+"/ -v "+var+" -c "+category+Opts[Unc]+" > "+DirName_datacard+"/datacard.log"
            print(command_run) 
            os.system(command_run)
