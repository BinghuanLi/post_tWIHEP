import sys, os, subprocess
import ROOT
from ROOT import TString, TFile, TTree
from threading import Thread

# please run this file in the same directory you put the datacards

cwd = os.getcwd()

frameworkDir = "/publicfs/cms/data/TopQuark/cms13TeV/Binghuan/ttH2019/condorStuff/rootplizers/combJobs/"
inputBaseDir = cwd 

Categories=["SubCat2l","DNNCat","DNNCat_option2","DNNCat_option3"]
varPerCat={
"SubCat2l":["Bin2l"],
"DNNCat":["DNN_maxval"],
"DNNCat_option2":["DNN_maxval_option2"],
"DNNCat_option3":["DNN_maxval_option3"],
}

regPerCat={
"SubCat2l":["2lss","ttWctrl"],
"DNNCat":["2lss"],
"DNNCat_option2":["2lss"],
"DNNCat_option3":["2lss"],
}

subCats={
#"SubCat2l":["inclusive","ee_neg","ee_pos", "em_bl_neg","em_bl_pos","em_bt_neg","em_bt_pos", "mm_bl_neg","mm_bl_pos","mm_bt_neg","mm_bt_pos" ]
"SubCat2l":["ee_neg","ee_pos", "em_bl_neg","em_bl_pos","em_bt_neg","em_bt_pos", "mm_bl_neg","mm_bl_pos","mm_bt_neg","mm_bt_pos" ],
"DNNCat":["ttHnode","ttJnode","ttWnode","ttZnode"],
"DNNCat_option2":["ttHnode","ttJnode","ttWnode","ttZnode"],
"DNNCat_option3":["ttHnode","ttJnode","ttWnode","ttZnode"],
}

def prepareCshJob(shFile,category, dirName):
    subFile      = file(shFile,"w")
    print >> subFile, "#!/bin/bash"
    print >> subFile, "/bin/hostname"
    print >> subFile, "source /cvmfs/sft.cern.ch/lcg/views/LCG_93/x86_64-slc6-gcc62-opt/setup.sh"
    print >> subFile, "gcc -v"
    print >> subFile, "pwd"
    print >> subFile, "cd "+dirName
    print >> subFile, "cmsenv"
    datacardName = "ttH"
    combineCards = "combineCards.py"
    for region in regPerCat[category]:
        datacardName += ("_"+region)
        for subCat in subCats[category]:
            combineCards += (" ttH_"+region+"_"+subCat+"=ttH_"+region+"_"+subCat+".txt")
    combineCards += (" > "+datacardName+".txt")
    print >> subFile, combineCards
    ExpLimit = "combine -M AsymptoticLimits "+datacardName + ".txt --expectSignal=1 -t -1 -m 125 > ExpLimit_"+datacardName+".log"
    print >> subFile, ExpLimit
    ExpSig = "combine -M FitDiagnostics --saveShapes --saveWithUncertainties --expectSignal=1 -t -1 "+datacardName + ".txt -m 125 > ExpSigStrength_"+datacardName+".log"
    print >> subFile, ExpSig 
    subprocess.call("chmod 777 "+shFile, shell=True)

allJobFile = 0
if os.path.exists(os.getcwd()+"/all.sh"):
    allJobFile = open(os.getcwd()+"/all.sh","a")
else:
    allJobFile = open(os.getcwd()+"/all.sh","w")
    allJobFile.write("#!/bin/bash\n")

for category in Categories:
    for var in varPerCat[category]:
        DirName_datacard = inputBaseDir+"/"+category+"/"+var
        shFileName = DirName_datacard + "/combineJob.sh"
        logFileName = DirName_datacard + "/combineJob.log"
        errorFileName = DirName_datacard + "/combineJob.error"
        prepareCshJob(shFileName, category, DirName_datacard)
        print >> allJobFile, "hep_sub "+ shFileName + " -o "+logFileName+ " -e "+errorFileName

allJobFile.close()
print "Finished " 
