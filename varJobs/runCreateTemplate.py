import sys, os, subprocess
import ROOT
from ROOT import TString, TFile, TTree
from threading import Thread



#Categories=["SubCat2l","DNNCat","DNNCat_option2","DNNCat_option3","DNNAMS2Cat1_option1","DNNAMS2Cat1_option2","DNNAMS2Cat1_option3","DNNAMS3Cat1_option1","DNNAMS3Cat1_option2","DNNAMS3Cat1_option3"]
#Categories=["SubCat2l","DNNCat","DNNCat_option2","DNNCat_option3","DNNSubCat1_option1","DNNSubCat1_option2","DNNSubCat1_option3","DNNSubCat2_option1","DNNSubCat2_option2","DNNSubCat2_option3"]
#Categories=["DNNCat","DNNSubCat1_option1","DNNSubCat2_option1"]
Categories=["DNNSubCat2_option1"]
#Categories=["SubCat2l","DNNCat","DNNCat_option2","DNNSubCat1_option1","DNNSubCat1_option2","DNNSubCat2_option1","DNNSubCat2_option2"]
#Categories=["DNNCat","DNNCat_option2"]
varPerCat={
"SubCat2l":["Bin2l"],
"DNNCat":["DNN_maxval"],
"DNNCat_option2":["DNN_maxval_option2"],
#"DNNCat_option2":["DNN_maxval_option2","Bin2l","leadLep_jetdr","secondLep_jetdr","n_presel_jet","nBJetLoose","nBJetMedium","jet1_pt","jet2_pt","jet3_pt","jet4_pt","jet1_eta","jet2_eta","jet3_eta","jet4_eta","Hj_tagger_resTop","metLD","maxeta","massL","avg_dr_jet","mbb","mT_lep1","mT_lep2","lep1_conePt","lep1_eta","lep2_conePt","lep2_eta","resTop_BDT"],
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

Uncs = ["All","NoShape"]
Opts = {
"All":" ",
"NoStat":" -m ",
"NoSyst":" -s ",
"NoShape":" -t ",
"None":" -s -m ",
}
version = "V0626_DNN_GT5"
inputDir = "Output"

for category in Categories:
    if not os.path.exists(inputDir+"/"+category+"/SystsDiLepRegion"):
        os.popen("mkdir -p "+inputDir+"/"+category+"/Systs2lss")
        os.popen("mkdir -p "+inputDir+"/"+category+"/SyststtWctrl")
        os.popen("mkdir -p "+inputDir+"/"+category+"/SystsDiLepRegion")
    for var in varPerCat[category]:
        DirName_datacard = version+"_datacards/"+category+"/"+var
        print ( "write histograms for var: "+var+ " in cat: "+ category)
        if not os.path.exists(DirName_datacard):
            os.popen("mkdir -p "+DirName_datacard)
        command_run = "python createDatacardRootFile.py -i "+inputDir+"/"+category+"/ -o "+DirName_datacard+"/ -v "+var+" -c "+category+" > "+DirName_datacard+"/Information.txt"
        print(command_run) 
        os.system(command_run)


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
