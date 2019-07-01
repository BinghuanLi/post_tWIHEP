import sys, os, subprocess
import ROOT
from ROOT import TString, TFile, TTree
from threading import Thread


#Categories=["SubCat2l","DNNCat","DNNCat_option2","DNNCat_option3","DNNSubCat1_option1","DNNSubCat1_option2","DNNSubCat1_option3","DNNSubCat2_option1","DNNSubCat2_option2","DNNSubCat2_option3"]
#Categories=["SubCat2l","DNNCat_option2","DNNSubCat1_option2","DNNSubCat2_option2"]
Categories=["DNNCat","DNNSubCat1_option1","DNNSubCat2_option1"]
#Categories=["DNNAMS2Cat1_option2"]

#Categories=["SubCat2l","DNNCat","DNNCat_option2","DNNCat_option3","DNNAMS2Cat1_option1","DNNAMS2Cat1_option2","DNNAMS2Cat1_option3","DNNAMS3Cat1_option1","DNNAMS3Cat1_option2","DNNAMS3Cat1_option3"]

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

regPerCat={
"SubCat2l":["DiLepRegion"],
"DNNCat":["DiLepRegion"],
"DNNCat_option2":["2lss","ttWctrl"],
"DNNCat_option3":["2lss","ttWctrl"],
"DNNSubCat1_option1":["DiLepRegion"],
"DNNSubCat1_option2":["2lss","ttWctrl"],
"DNNSubCat1_option3":["2lss","ttWctrl"],
"DNNSubCat2_option1":["DiLepRegion"],
"DNNSubCat2_option2":["2lss","ttWctrl"],
"DNNSubCat2_option3":["2lss","ttWctrl"],
"DNNAMS2Cat1_option1":["2lss","ttWctrl"],
"DNNAMS2Cat1_option2":["2lss","ttWctrl"],
"DNNAMS2Cat1_option3":["2lss","ttWctrl"],
"DNNAMS3Cat1_option1":["2lss","ttWctrl"],
"DNNAMS3Cat1_option2":["2lss","ttWctrl"],
"DNNAMS3Cat1_option3":["2lss","ttWctrl"],
}

subCats={
#"SubCat2l":["inclusive","ee_neg","ee_pos", "em_bl_neg","em_bl_pos","em_bt_neg","em_bt_pos", "mm_bl_neg","mm_bl_pos","mm_bt_neg","mm_bt_pos" ]
"SubCat2l":["ee_neg","ee_pos", "em_bl_neg","em_bl_pos","em_bt_neg","em_bt_pos", "mm_bl_neg","mm_bl_pos","mm_bt_neg","mm_bt_pos" ],
"DNNCat":["ttHnode","ttJnode","ttWnode","ttZnode"],
"DNNCat_option2":["ttHnode","ttJnode","ttWnode","ttZnode"],
"DNNCat_option3":["ttHnode","ttJnode","ttWnode","ttZnode"],
"DNNSubCat1_option1":["ee_neg","ee_pos","em_ttHnode","em_ttJnode","em_ttWnode","em_ttZnode","mm_ttHnode","mm_ttJnode","mm_ttWnode","mm_ttZnode"],
"DNNSubCat1_option2":["ee_neg","ee_pos","em_ttHnode","em_ttJnode","em_ttWnode","em_ttZnode","mm_ttHnode","mm_ttJnode","mm_ttWnode","mm_ttZnode"],
"DNNSubCat1_option3":["ee_neg","ee_pos","em_ttHnode","em_ttJnode","em_ttWnode","em_ttZnode","mm_ttHnode","mm_ttJnode","mm_ttWnode","mm_ttZnode"],
"DNNSubCat2_option1":["ee_ttHnode","ee_ttJnode","ee_ttWnode","ee_ttZnode","em_ttHnode","em_ttJnode","em_ttWnode","em_ttZnode","mm_ttHnode","mm_ttJnode","mm_ttWnode","mm_ttZnode"],
"DNNSubCat2_option2":["ee_ttHnode","ee_ttJnode","ee_ttWnode","ee_ttZnode","em_ttHnode","em_ttJnode","em_ttWnode","em_ttZnode","mm_ttHnode","mm_ttJnode","mm_ttWnode","mm_ttZnode"],
"DNNSubCat2_option3":["ee_ttHnode","ee_ttJnode","ee_ttWnode","ee_ttZnode","em_ttHnode","em_ttJnode","em_ttWnode","em_ttZnode","mm_ttHnode","mm_ttJnode","mm_ttWnode","mm_ttZnode"],
"DNNAMS2Cat1_option1":["loose_ttHnode","tight_ttHnode","ttJnode","ttWnode","ttZnode"],
"DNNAMS2Cat1_option2":["loose_ttHnode","tight_ttHnode","ttJnode","ttWnode","ttZnode"],
"DNNAMS2Cat1_option3":["loose_ttHnode","tight_ttHnode","ttJnode","ttWnode","ttZnode"],
"DNNAMS3Cat1_option1":["loose_ttHnode","tight_ttHnode","ttJnode","ttWnode","ttZnode"],
"DNNAMS3Cat1_option2":["loose_ttHnode","tight_ttHnode","ttJnode","ttWnode","ttZnode"],
"DNNAMS3Cat1_option3":["loose_ttHnode","tight_ttHnode","ttJnode","ttWnode","ttZnode"],
}

dirName = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/rootplasDNN_20190613_LongerFully/Rootplas/Output_GT3/"

blind ="1"
latex ="0"

for category in Categories:
    for var in varPerCat[category]:
        print ( "plot var: "+var+ " in cat: "+ category)
        for reg in regPerCat[category]:
            for channel in subCats[category]:
                command_run = "python stackplot.py -r "+reg+" -p "+var+" -c "+category+" -d "+dirName + " -l "+latex+" -s "+channel + " -b "+ blind 
                print(command_run) 
                os.system(command_run)
