import sys, os, subprocess
import ROOT
from ROOT import TString, TFile, TTree
from threading import Thread


#Categories=["SubCat2l","DNNCat","DNNCat_option2","DNNCat_option3","DNNAMS2Cat1_option1","DNNAMS2Cat1_option2","DNNAMS2Cat1_option3","DNNAMS3Cat1_option1","DNNAMS3Cat1_option2","DNNAMS3Cat1_option3"]
#Categories=["DNNCat","DNNSubCat1_option1","DNNSubCat2_option1"]
#Categories=["DNNSubCat2_option1"]
Categories=["SubCat2l"]
#Uncs = ["All","NoStat","NoSyst","None","NoShape"]
Uncs = ["All"]
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

systs_ctcvcp = [
"","kt_m3_kv_1","kt_m2_kv_1","kt_m1p5_kv_1","kt_m1p25_kv_1","kt_m0p75_kv_1","kt_m0p5_kv_1","kt_m0p25_kv_1","kt_0_kv_1","kt_0p25_kv_1","kt_0p5_kv_1","kt_0p75_kv_1","kt_1_kv_1","kt_1p25_kv_1","kt_1p5_kv_1","kt_2_kv_1","kt_3_kv_1","kt_m2_kv_1p5","kt_m1p5_kv_1p5","kt_m1p25_kv_1p5","kt_m1_kv_1p5","kt_m0p5_kv_1p5","kt_m0p25_kv_1p5","kt_0p25_kv_1p5","kt_0p5_kv_1p5","kt_1_kv_1p5","kt_1p25_kv_1p5","kt_m3_kv_0p5","kt_m2_kv_0p5","kt_m1p25_kv_0p5","kt_1p25_kv_0p5","kt_2_kv_0p5","kt_3_kv_0p5","cosa_m0p9","cosa_m0p8","cosa_m0p7","cosa_m0p6","cosa_m0p5","cosa_m0p4","cosa_m0p3","cosa_m0p2","cosa_m0p1","cosa_mp0","cosa_0p1","cosa_0p2","cosa_0p3","cosa_0p4","cosa_0p5","cosa_0p6","cosa_0p7","cosa_0p8","cosa_0p9"
]

year = 2016
version = "V0927_test_%i"%year

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
            for syst_ctcvcp in systs_ctcvcp:
                syst_ctcvcp = "_" + syst_ctcvcp
                command_run = "python datacard_Template.py -i "+version+"_datacards_"+Unc+"/ -v "+var+" -c "+category+Opts[Unc]+ " -p "+ syst_ctcvcp + " -y " + str(year) +  " > "+DirName_datacard+"/datacard.log"
                print(command_run) 
                os.system(command_run)
