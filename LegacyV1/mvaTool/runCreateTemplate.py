import sys, os, subprocess
import ROOT
from ROOT import TString, TFile, TTree
from threading import Thread



#Categories=["SubCat2l","DNNCat","DNNCat_option2","DNNCat_option3","DNNAMS2Cat1_option1","DNNAMS2Cat1_option2","DNNAMS2Cat1_option3","DNNAMS3Cat1_option1","DNNAMS3Cat1_option2","DNNAMS3Cat1_option3"]
#Categories=["SubCat2l","DNNCat","DNNCat_option2","DNNCat_option3","DNNSubCat1_option1","DNNSubCat1_option2","DNNSubCat1_option3","DNNSubCat2_option1","DNNSubCat2_option2","DNNSubCat2_option3"]
#Categories=["DNNCat","DNNSubCat1_option1","DNNSubCat2_option1"]
Categories=["DNNSubCat2_option1","SubCat2l"]
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
#"DNNSubCat2_option1":["DNN_maxval"],
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

Uncs = ["All"]
Opts = {
"All":" ",
"NoStat":" -m ",
"NoSyst":" -s ",
"NoShape":" -t ",
"None":" -s -m ",
}


#years=[2016,2017,2018]
years=[2017,2018]
namefix= ["datacard","tHq"] # "datacard" for normal usage, "tHq" for kt kv usage
createROOT= True

systs_ctcvcp = [
"kt_m3_kv_1","kt_m2_kv_1","kt_m1p5_kv_1","kt_m1p25_kv_1","kt_m0p75_kv_1","kt_m0p5_kv_1","kt_m0p25_kv_1","kt_0_kv_1","kt_0p25_kv_1","kt_0p5_kv_1","kt_0p75_kv_1","kt_1_kv_1","kt_1p25_kv_1","kt_1p5_kv_1","kt_2_kv_1","kt_3_kv_1","kt_m2_kv_1p5","kt_m1p5_kv_1p5","kt_m1p25_kv_1p5","kt_m1_kv_1p5","kt_m0p5_kv_1p5","kt_m0p25_kv_1p5","kt_0p25_kv_1p5","kt_0p5_kv_1p5","kt_1_kv_1p5","kt_1p25_kv_1p5","kt_2_kv_1p5","kt_m3_kv_0p5","kt_m2_kv_0p5","kt_m1p25_kv_0p5","kt_1p25_kv_0p5","kt_2_kv_0p5","kt_3_kv_0p5",
#"cosa_m0p9","cosa_m0p8","cosa_m0p7","cosa_m0p6","cosa_m0p5","cosa_m0p4","cosa_m0p3","cosa_m0p2","cosa_m0p1","cosa_mp0","cosa_0p1","cosa_0p2","cosa_0p3","cosa_0p4","cosa_0p5","cosa_0p6","cosa_0p7","cosa_0p8","cosa_0p9"
]

for year in years:
    version = "DiLepRegion_RunII_%i_V1025.2"%year
    inputDir = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/mvaTool_LegacyAll_20191025_v3/Output_%i_GT5"%year

    if createROOT :
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
            for name in namefix:
                command_run = "python createDatacardRootFile.py -s 0 -i "+inputDir+"/"+category+"/ -o "+DirName_datacard+"/ -v "+var+" -c "+category+ " -y " + str(year)+ " -n "+ name +" > "+DirName_datacard+"/Information.txt"
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
                for name in namefix:
                    if "tHq" in name:
                        for syst_ctcvcp in systs_ctcvcp:
                            syst_ctcvcp = "_" + syst_ctcvcp
                            command_run = "python datacard_Template.py -i "+version+"_datacards_"+Unc+"/ -v "+var+" -c "+category+Opts[Unc]+ " -p "+ syst_ctcvcp + " -y " + str(year) +" -n " + name +" > "+DirName_datacard+"/datacard.log"
                            print(command_run) 
                            os.system(command_run)
                    else:
                        command_run = "python datacard_Template.py -i "+version+"_datacards_"+Unc+"/ -v "+var+" -c "+category+Opts[Unc]+ "-p _ -y " + str(year) +" -n " + name +" > "+DirName_datacard+"/datacard.log"
                        print(command_run) 
                        os.system(command_run)
