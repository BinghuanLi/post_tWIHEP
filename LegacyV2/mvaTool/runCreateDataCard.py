import sys, os, subprocess
import ROOT
from ROOT import TString, TFile, TTree
from threading import Thread



#Categories=["SubCat2l","DNNCat","DNNCat_option2","DNNCat_option3","DNNAMS2Cat1_option1","DNNAMS2Cat1_option2","DNNAMS2Cat1_option3","DNNAMS3Cat1_option1","DNNAMS3Cat1_option2","DNNAMS3Cat1_option3"]
#Categories=["SubCat2l","DNNCat","DNNCat_option2","DNNCat_option3","DNNSubCat1_option1","DNNSubCat1_option2","DNNSubCat1_option3","DNNSubCat2_option1","DNNSubCat2_option2","DNNSubCat2_option3"]
#Categories=["DNNCat","DNNSubCat1_option1","DNNSubCat2_option1"]
Categories=["SubCat2l","DNNSubCat2_option1"]
#Categories=["DNNCat","DNNCat_option2"]
#Categories=["SubCat2l"]
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

year = 2016
version = "V0927_test_%i"%year
inputDir = "Output_%i_GT5"%year

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
        command_run = "python createDatacardRootFile.py -s 0 -i "+inputDir+"/"+category+"/ -o "+DirName_datacard+"/ -v "+var+" -c "+category+ " -y "+str(year)+" > "+DirName_datacard+"/Information.txt"
        print(command_run) 
        os.system(command_run)
