import sys, os, subprocess
import ROOT
from ROOT import TString, TFile, TTree
from threading import Thread

# please run this file in the same directory you put the datacards

cwd = os.getcwd()

frameworkDir = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/rootplizers/combJobs/"
inputBaseDir = cwd 

makeImpact = True
impact = "estimateImpact_expected.sh"

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

regPerCat={
"SubCat2l":["2lss","ttWctrl"],
"DNNCat":["2lss","ttWctrl"],
"DNNCat_option2":["2lss","ttWctrl"],
"DNNCat_option3":["2lss","ttWctrl"],
"DNNSubCat1_option1":["2lss","ttWctrl"],
"DNNSubCat1_option2":["2lss","ttWctrl"],
"DNNSubCat1_option3":["2lss","ttWctrl"],
"DNNSubCat2_option1":["2lss","ttWctrl"],
"DNNSubCat2_option2":["2lss","ttWctrl"],
"DNNSubCat2_option3":["2lss","ttWctrl"],
#"SubCat2l":["2lss"],
#"DNNCat":["2lss"],
#"DNNCat_option2":["2lss"],
#"DNNCat_option3":["2lss"],
#"DNNSubCat1_option1":["2lss"],
#"DNNSubCat1_option2":["2lss"],
#"DNNSubCat1_option3":["2lss"],
#"DNNSubCat2_option1":["2lss"],
#"DNNSubCat2_option2":["2lss"],
#"DNNSubCat2_option3":["2lss"],
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
}

def prepareCshJob(shFile,category, dirName):
    subFile      = file(shFile,"w")
    print >> subFile, "#!/bin/bash"
    print >> subFile, "/bin/hostname"
    print >> subFile, "gcc -v"
    print >> subFile, "pwd"
    print >> subFile, "cd "+dirName+"/"
    print >> subFile, "eval `scramv1 runtime -sh`"
    datacardName = "ttH"
    combineCards = "combineCards.py"
    for region in regPerCat[category]:
        datacardName += ("_"+region)
        for subCat in subCats[category]:
            count = 0
            datacard = open(dirName+"/ttH_"+region+"_"+subCat+".txt",'r').read()
            count = datacard.count("ttH_"+region+"_"+subCat)
            if count <3: continue
            combineCards += (" ttH_"+region+"_"+subCat+"=ttH_"+region+"_"+subCat+".txt")
    combineCards += (" > "+datacardName+".txt")
    print >> subFile, combineCards
    ExpLimit = "combine -M AsymptoticLimits "+datacardName + ".txt --expectSignal=1 -t -1 -m 125 > ExpLimit_"+datacardName+".log"
    print >> subFile, ExpLimit
    ExpSig = "combine -M FitDiagnostics --saveShapes --saveWithUncertainties --expectSignal=1 -t -1 "+datacardName + ".txt -m 125 > ExpSigStrength_"+datacardName+".log"
    print >> subFile, ExpSig
    if makeImpact:
        ExpImpact = "./"+impact+" "+datacardName 
        print >> subFile, ExpImpact
    subprocess.call("chmod 777 "+shFile, shell=True)

allJobFile = 0
if os.path.exists(os.getcwd()+"/all.sh"):
    allJobFile = open(os.getcwd()+"/all.sh","a")
else:
    allJobFile = open(os.getcwd()+"/all.sh","w")
    allJobFile.write("#!/bin/bash\n")

for category in Categories:
    for var in varPerCat[category]:
        fix =""
        for regionName in regPerCat[category]:
            fix += ("_"+regionName)
        DirName_datacard = inputBaseDir+"/"+category+"/"+var
        shFileName = DirName_datacard + "/Fit_"+category+"_"+var+fix+"_Job.sh"
        logFileName = DirName_datacard + "/Fit_"+category+"_"+var+fix+"_Job.log"
        errorFileName = DirName_datacard + "/Fit_"+category+"_"+var+fix+"_Job.error"
        prepareCshJob(shFileName, category, DirName_datacard)
        command_cp = "cp "+frameworkDir+impact+" "+DirName_datacard
        print(command_cp)
        os.system(command_cp)
        print >> allJobFile, "hep_sub "+ shFileName + " -o "+logFileName+ " -e "+errorFileName

allJobFile.close()
print "Finished " 
